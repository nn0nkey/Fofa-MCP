#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Uncover MCP Server - Correct Version
Author: nn0nkey
MCP service implementation for discovering exposed hosts using Shodan and FOFA
"""

import asyncio
import json
import os
import sys
from typing import Any, Dict, List, Optional
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import (
        CallToolRequest,
        CallToolResult,
        ListToolsRequest,
        ListToolsResult,
        Tool,
        TextContent,
    )
except ImportError:
    print("Error: Please install MCP Python SDK")
    print("pip install mcp")
    sys.exit(1)

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError:
    print("Error: Please install requests library")
    print("pip install requests")
    sys.exit(1)


class UncoverMCPServer:
    """Uncover MCP Server Class"""
    
    def __init__(self):
        self.server = Server("uncover-mcp")
        self.setup_handlers()
        
        # Configure request retry
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # API configuration
        self.shodan_api_key = os.getenv("SHODAN_API_KEY", "")
        self.fofa_email = os.getenv("FOFA_EMAIL", "")
        self.fofa_key = os.getenv("FOFA_KEY", "")
    
    def setup_handlers(self):
        """Setup MCP handlers"""
        
        @self.server.list_tools()
        async def list_tools() -> ListToolsResult:
            """List available tools"""
            tools = [
                Tool(
                    name="shodan",
                    description="Use Shodan search engine to find exposed hosts",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Shodan search query"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Limit the number of results",
                                "default": 100
                            },
                            "field": {
                                "type": "string",
                                "description": "Return field format (ip:port, host, ip, port)",
                                "default": "ip:port"
                            }
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="fofa",
                    description="Use FOFA search engine to find exposed hosts",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "FOFA search query"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Limit the number of results",
                                "default": 100
                            },
                            "field": {
                                "type": "string",
                                "description": "Return field format (ip:port, host, ip, port)",
                                "default": "ip:port"
                            }
                        },
                        "required": ["query"]
                    }
                )
            ]
            return ListToolsResult(tools=tools)
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]):
            """Call a tool"""
            if name == "shodan":
                return await self.handle_shodan(arguments)
            elif name == "fofa":
                return await self.handle_fofa(arguments)
            else:
                return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    async def handle_shodan(self, arguments: Dict[str, Any]):
        """Handle Shodan search requests"""
        if not self.shodan_api_key:
            raise Exception("SHODAN_API_KEY environment variable not set")
        
        query = arguments.get("query", "")
        limit = arguments.get("limit", 100)
        field = arguments.get("field", "ip:port")
        
        if not query:
            raise Exception("Query cannot be empty")
        
        results = await self.search_shodan(query, limit)
        formatted_results = self.format_results(results, field)
        
        return [TextContent(type="text", text=formatted_results)]
    
    async def handle_fofa(self, arguments: Dict[str, Any]):
        """Handle FOFA search requests"""
        if not self.fofa_email or not self.fofa_key:
            raise Exception("FOFA_EMAIL and FOFA_KEY environment variables not set")
        
        query = arguments.get("query", "")
        limit = arguments.get("limit", 100)
        field = arguments.get("field", "ip:port")
        
        if not query:
            raise Exception("Query cannot be empty")
        
        results = await self.search_fofa(query, limit)
        formatted_results = self.format_results(results, field)
        
        return [TextContent(type="text", text=formatted_results)]
    
    async def search_shodan(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Execute Shodan search"""
        url = "https://api.shodan.io/shodan/host/search"
        params = {
            "key": self.shodan_api_key,
            "query": query,
            "minify": True
        }
        
        results = []
        page = 1
        
        while len(results) < limit:
            params["page"] = page
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            matches = data.get("matches", [])
            
            if not matches:
                break
            
            for match in matches:
                if len(results) >= limit:
                    break
                results.append({
                    "ip": match.get("ip_str", ""),
                    "port": match.get("port", 0),
                    "hostnames": match.get("hostnames", []),
                    "domains": match.get("domains", []),
                    "location": match.get("location", {})
                })
            
            page += 1
        
        return results[:limit]
    
    async def search_fofa(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Execute FOFA search"""
        # FOFA API needs to get token first
        auth_url = "https://fofa.info/api/v1/info/my"
        auth_params = {
            "email": self.fofa_email,
            "key": self.fofa_key
        }
        
        # Get user info to verify API key
        auth_response = self.session.get(auth_url, params=auth_params, timeout=30)
        auth_response.raise_for_status()
        
        # Execute search
        search_url = "https://fofa.info/api/v1/search/all"
        search_params = {
            "email": self.fofa_email,
            "key": self.fofa_key,
            "qbase64": self.encode_base64(query),
            "size": min(limit, 10000),  # FOFA max 10000 per request
            "fields": "ip,port,host,domain,title,server,protocol,country,region,city"
        }
        
        response = self.session.get(search_url, params=search_params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        if not data.get("error"):
            results = []
            for item in data.get("results", []):
                if len(results) >= limit:
                    break
                results.append({
                    "ip": item[0] if len(item) > 0 else "",
                    "port": int(item[1]) if len(item) > 1 and item[1].isdigit() else 0,
                    "host": item[2] if len(item) > 2 else "",
                    "domain": item[3] if len(item) > 3 else "",
                    "title": item[4] if len(item) > 4 else "",
                    "server": item[5] if len(item) > 5 else "",
                    "protocol": item[6] if len(item) > 6 else "",
                    "country": item[7] if len(item) > 7 else "",
                    "region": item[8] if len(item) > 8 else "",
                    "city": item[9] if len(item) > 9 else ""
                })
            return results
        else:
            raise Exception(f"FOFA API error: {data.get('errmsg', 'Unknown error')}")
    
    def encode_base64(self, text: str) -> str:
        """Base64 encode"""
        import base64
        return base64.b64encode(text.encode('utf-8')).decode('utf-8')
    
    def format_results(self, results: List[Dict[str, Any]], field: str) -> str:
        """Format results"""
        if not results:
            return "No results found"
        
        formatted = []
        for result in results:
            if field == "ip:port":
                formatted.append(f"{result.get('ip', '')}:{result.get('port', '')}")
            elif field == "host":
                host = result.get('host', '') or result.get('hostnames', [''])[0] if result.get('hostnames') else ''
                formatted.append(host)
            elif field == "ip":
                formatted.append(result.get('ip', ''))
            elif field == "port":
                formatted.append(str(result.get('port', '')))
            else:
                # Default format with more info
                ip = result.get('ip', '')
                port = result.get('port', '')
                host = result.get('host', '') or (result.get('hostnames', [''])[0] if result.get('hostnames') else '')
                formatted.append(f"{ip}:{port} {host}")
        
        return "\n".join(formatted)


async def main():
    """Main function"""
    # Create server instance
    uncover_server = UncoverMCPServer()
    
    # Check API keys
    if not uncover_server.shodan_api_key and not uncover_server.fofa_email:
        logger.warning("Warning: No API keys set, some features may not be available")
        logger.info("Please set the following environment variables:")
        logger.info("  SHODAN_API_KEY - Shodan API key")
        logger.info("  FOFA_EMAIL - FOFA email")
        logger.info("  FOFA_KEY - FOFA API key")
    
    # Start server
    logger.info("Starting Uncover MCP server...")
    logger.info("Author: nn0nkey")
    logger.info("Supported search engines: Shodan, FOFA")
    
    async with stdio_server() as (read_stream, write_stream):
        await uncover_server.server.run(
            read_stream,
            write_stream,
            uncover_server.server.create_initialization_options()
        )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)
