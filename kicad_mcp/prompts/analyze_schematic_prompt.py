"""
Schematic-related prompt template for KiCad.
"""
from mcp.server.fastmcp import FastMCP


def register_schematic_prompts(mcp: FastMCP) -> None:
    """Register Schematic-related prompt templates with the MCP server.
    
    Args:
        mcp: The FastMCP server instance
    """
    
    @mcp.prompt()
    def analyze_schematic() -> str:
        """Prompt for analyzing a KiCad project's schematic File."""

        prompt = """
        You are conducting a systematic, exhaustive hardware design review. Your analysis must be methodical and complete - missing any significant issue reflects a failure in the review process. Follow this structured approach:
        Phase 1: Component-by-Component Analysis
        For EVERY component in the schematic:
        A. Power Components (MCUs, ICs, etc.)

        Pin-by-pin verification: Check EVERY pin - power, ground, I/O, special functions
        Missing support circuits: Decoupling caps, pull-ups/downs, terminations, filters
        Power sequencing: Verify all power domains are properly handled
        Reference voltages: Check AREF, VREF, and analog supply filtering
        Special pins: Boot pins, enable pins, reset pins, crystal connections

        B. Passive Components

        Value verification: Are R/C/L values appropriate for their function?
        Missing components: Current limiting, filtering, protection, termination
        Component relationships: Series/parallel combinations, divider networks
        Power ratings: Adequate for expected current/voltage

        C. Interface Components

        Connectors: Pin assignments, power delivery, signal integrity
        Protection: ESD, overcurrent, reverse polarity
        Termination: Impedance matching, pull-ups/downs
        Standards compliance: USB, I2C, SPI, UART specifications

        Phase 2: Net-by-Net Analysis
        For EVERY net in the design:
        A. Signal Integrity

        Drive capability: Can source drive all loads?
        Loading analysis: Input impedance, capacitive loading
        Voltage levels: Logic level compatibility
        Timing: Setup/hold times, propagation delays

        B. Power Distribution

        Current capacity: Wire gauge, trace width, connector ratings
        Voltage regulation: Dropout, load regulation, ripple
        Decoupling strategy: Local, bulk, and high-frequency decoupling
        Ground integrity: Ground loops, ground bounce, reference issues

        C. Interconnection Logic

        Signal routing: Point-to-point verification vs. schematic intent
        Unintended connections: Shorts, floating nodes, ground loops
        Interface mismatches: Voltage, impedance, protocol compatibility

        Phase 3: Circuit Topology Analysis
        For EVERY functional block:
        A. Current Path Analysis

        Complete current loops: From source through load to return
        Current limiting: Adequate protection for all paths
        Current sharing: Parallel elements, load balancing
        Fault currents: Short circuit protection, current limiting

        B. Voltage Level Analysis

        Voltage drops: Series resistance, diode drops, cable losses
        Voltage dividers: Ratio verification, loading effects
        Level shifting: Inter-domain communication
        Margin analysis: Worst-case voltage scenarios

        C. Impedance Analysis

        Input/output impedance: Matching, loading, reflection
        Transmission lines: Controlled impedance, termination
        AC coupling: Frequency response, DC blocking
        Filtering: Cutoff frequencies, attenuation, group delay

        Phase 4: Standards and Best Practices
        Check against industry standards:
        A. Design Rules

        Manufacturer recommendations: Datasheet application circuits
        Industry standards: USB, PCIe, Ethernet, etc.
        EMC compliance: Filtering, grounding, shielding
        Safety standards: Isolation, protection, current limits

        B. Component Selection

        Specification verification: Ratings vs. application requirements
        Tolerance analysis: Worst-case component variations
        Reliability factors: Derating, lifecycle, MTBF
        Availability: Standard parts, obsolescence risk

        Phase 5: Missing Elements Detection
        Actively search for missing:
        A. Protection Circuits

        ESD protection: TVS diodes, ferrite beads
        Overcurrent protection: Fuses, current limiters
        Overvoltage protection: Zener clamps, voltage supervisors
        Reverse polarity protection: Diodes, MOSFETs

        B. Support Circuits

        Reset circuits: Power-on reset, watchdog, manual reset
        Clock circuits: Crystals, load caps, termination
        Programming interfaces: ISP, JTAG, SWD headers
        Test points: Debug access, measurement points

        C. Interface Requirements

        Pull-up/pull-down resistors: Open drain, I2C, configuration pins
        Termination resistors: Differential signals, transmission lines
        Coupling components: AC coupling caps, isolation transformers
        Filtering components: EMI filters, anti-aliasing filters

        Reporting Structure
        For each issue found, provide:

        Component/Net/Pin identification
        Issue severity: Critical/High/Medium/Low
        Problem description: What's wrong and why
        Impact analysis: What will happen if not fixed
        Specific fix: Exact component values and connections
        Design rationale: Why this fix is the best approach

        Verification Checklist
        Before completing the review, verify you have:

        Analyzed every component in the BOM/netlist
        Checked every net for proper connections
        Verified every IC pin has proper support circuitry
        Confirmed all interfaces meet their specifications
        Identified all missing protection and support circuits
        Calculated critical parameters (current, voltage, impedance)
        Cross-referenced against manufacturer application notes
        Considered manufacturing, testing, and debug requirements

        Success Criteria
        A successful review will:

        Find ALL significant issues in a single pass
        Provide specific, actionable fixes for each problem
        Explain the engineering rationale behind each recommendation
        Prioritize issues by impact on functionality and reliability
        Consider the complete product lifecycle from prototype to production

        Failure Indicators
        The review has failed if:

        Significant issues are discovered in subsequent analysis
        Recommendations lack specific component values or connections
        Critical safety or functionality issues are missed
        Industry standard practices are not followed
        Missing components prevent basic circuit operation

        """