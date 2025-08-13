import subprocess
import sys

def analyze_scan_output(scan_output, ip_address):
    """
    Analyzes the plain text output from Nmap to find and display vulnerabilities.

    Args:
        scan_output (str): The raw text output from the Nmap command.
        ip_address (str): The IP address that was scanned.
    """
    print(f"\n--- Scan Report for {ip_address} ---")
    
    vulnerabilities_found = []
    # Split the output into individual lines to check for vulnerability info
    lines = scan_output.split('\n')
    
    # A simple way to find vulnerability script output is to look for lines
    # that Nmap formats with a '|' or '_' at the beginning of the finding.
    for line in lines:
        # We check if the stripped line starts with these characters
        if line.strip().startswith(('|', '_')):
            # Add the finding to our list
            vulnerabilities_found.append(line.strip())

    if vulnerabilities_found:
        print("\n[+] Vulnerabilities Found:")
        for vuln in vulnerabilities_found:
            print(f"    {vuln}")
        print("\n[+] Security Feedback: Vulnerabilities detected. Please review the details above.")
    else:
        print("\n[+] Security Feedback: No obvious vulnerabilities were found with this scan.")
        
    print(f"----------------------------------------")


def main():
    """
    Main function to run the network scan on a single IP.
    """
    target_ip = input("Enter the IP address to scan (e.g., 192.168.1.1 or scanme.nmap.org): ")
    if not target_ip:
        print("[-] Error: No IP address provided. Exiting.")
        return

    print(f"\n[+] Starting Nmap scan on {target_ip}. This may take a while...")

    try:
        # Simplified command: -sV for version detection and --script vuln for vulnerability scanning.
        command = ["sudo", "nmap", "-sV", "--script", "vuln", target_ip]
        
        # Run the command and capture the output as text.
        result = subprocess.run(
            command, 
            capture_output=True, 
            text=True, 
            check=False # We handle errors manually
        )

        # If the command failed and there's no output, print the error.
        if result.returncode != 0 and not result.stdout.strip():
            print("[-] Nmap command failed. Please ensure Nmap is installed and you have sudo privileges.")
            print(f"[-] Error details: {result.stderr}")
            return
        
        # Pass the text output to our analysis function
        analyze_scan_output(result.stdout, target_ip)

    except FileNotFoundError:
        print("[-] Error: 'nmap' command not found. Please install Nmap on your system.")
    except Exception as e:
        print(f"[!] An unexpected error occurred: {e}")


if __name__ == "__main__":
    # Check for root privileges before running, as Nmap needs them for many scan types.
    if sys.platform != "win32" and subprocess.os.geteuid() != 0:
        print("[-] This script requires root privileges. Please run it with 'sudo'.")
        sys.exit(1)
    main()
