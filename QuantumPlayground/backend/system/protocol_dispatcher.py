import os
from backend.handlers import (
    abp_handler,
    abp_stream_reader,
    mcp_loader,
    a2a_handler
)

def dispatch_protocol_file(file_path):
    extension = os.path.splitext(file_path)[1].lower()

    match extension:
        case ".abp":
            print("[DISPATCH] Routing to ABP stream reader...")
            abp_stream_reader.read_abp_stream(file_path)

        case ".mcp":
            print("[DISPATCH] Routing to MCP loader...")
            mcp_loader.load_mcp_context(file_path)

        case ".a2a":
            print("[DISPATCH] Routing to A2A handler...")
            a2a_handler.process_a2a_stream(file_path)

        case _:
            print(f"[DISPATCH] Unknown or unsupported protocol: {extension}")