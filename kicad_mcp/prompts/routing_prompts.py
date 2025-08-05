"""
Prompts for plcaing routes in kicad.
"""
from mcp.server.fastmcp import FastMCP


def register_routing_prompts(mcp: FastMCP) -> None:
    """Register routing-related prompt templates with the MCP server.
    
    Args:
        mcp: The FastMCP server instance
    """
    
    @mcp.prompt()
    def generate_pcb_routes() -> str:
        """Prompt for generating PCB routing paths in KiCad."""

        prompt = """
        You are an intelligent PCB routing assistant. Your goal is to generate clean, manufacturable, and electrically sound routes between component pads on a KiCad PCB layout. When creating routes, follow these rules:

        1. Routing Geometry:
           - Prefer 45-degree angles for all trace bends.
           - Avoid 90-degree corners; instead, use two 45° segments for direction changes.

        2. Design Rule Compliance:
           - Follow standard trace width and clearance rules defined in the board settings.
           - Avoid routing too close to pads, vias, or the board edge.

        3. Noise & Signal Integrity:
           - Keep high-speed or sensitive signals short and avoid routing them near noisy nets (like clocks or power).
           - Route differential pairs together with constant spacing.
           - Avoid sharp turns on impedance-critical traces.

        4. Power & Ground:
           - Prefer wide traces for power and ground, or use polygons (zones) for distribution.
           - Minimize loops in return paths and ensure solid grounding where possible.


        Generate routing paths that follow these principles, given source and destination pads or coordinates, layer, width, and net name.
        """
        
        return prompt
    