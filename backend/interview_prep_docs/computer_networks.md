# Computer Networks Interview Q&A

## Question: What is the difference between TCP and UDP?
TCP (Transmission Control Protocol) is connection-oriented, reliable, ensures ordered delivery with error checking and retransmission, but has more overhead — used for web browsing (HTTP), file transfer, email. UDP (User Datagram Protocol) is connectionless, faster with lower overhead, but doesn't guarantee delivery or order — used for video streaming, DNS lookups, online gaming, where speed matters more than perfect reliability.

## Question: Explain the OSI model layers briefly.
Physical (raw bit transmission over hardware), Data Link (framing, MAC addresses, error detection on a local network), Network (routing, IP addressing, packet forwarding across networks), Transport (end-to-end delivery, TCP/UDP, ports), Session (managing connections/sessions between applications), Presentation (data translation, encryption, compression), Application (user-facing protocols like HTTP, FTP, SMTP). Mnemonic: "Please Do Not Throw Sausage Pizza Away."

## Question: What happens when you type a URL into a browser and press enter?
Browser checks cache for a cached DNS/response; DNS resolution converts the domain to an IP address; a TCP connection is established with the server (three-way handshake); if HTTPS, a TLS handshake negotiates encryption; the browser sends an HTTP GET request; the server processes it and sends back an HTTP response with the HTML; the browser parses HTML, fetches additional resources (CSS/JS/images), and renders the page.

## Question: What is the difference between HTTP and HTTPS?
HTTP transmits data in plain text between client and server, making it vulnerable to interception. HTTPS adds a TLS/SSL encryption layer on top of HTTP, encrypting data in transit and verifying server identity via certificates, protecting against eavesdropping and man-in-the-middle attacks. HTTPS uses port 443 by default versus HTTP's port 80.

## Question: What is a three-way handshake in TCP?
It's the process to establish a reliable TCP connection: (1) client sends a SYN (synchronize) packet to the server, (2) server responds with a SYN-ACK (synchronize-acknowledge) packet, (3) client responds with an ACK (acknowledge) packet. After this exchange, both sides agree the connection is established and data transfer can begin.

## Question: What is DNS and how does DNS resolution work?
DNS (Domain Name System) translates human-readable domain names into IP addresses. Resolution flow: browser checks local cache, then queries a recursive resolver (usually from your ISP), which queries a root nameserver, then a TLD nameserver (e.g., .com), then the authoritative nameserver for the specific domain, which returns the actual IP address — this result gets cached at multiple levels for future speed.

## Question: What is the difference between a router, switch, and hub?
A hub is a basic device that broadcasts incoming data to all connected devices on a network (no intelligence, causes collisions). A switch operates at the Data Link layer, intelligently forwarding data only to the specific device (using MAC addresses) it's intended for within a local network. A router operates at the Network layer, connecting different networks together and directing data packets between them based on IP addresses.

## Question: What are HTTP status code categories?
1xx (Informational) — request received, continuing process. 2xx (Success) — e.g., 200 OK, 201 Created. 3xx (Redirection) — e.g., 301 Moved Permanently, 304 Not Modified. 4xx (Client Error) — e.g., 400 Bad Request, 401 Unauthorized, 404 Not Found. 5xx (Server Error) — e.g., 500 Internal Server Error, 503 Service Unavailable.

## Question: What is the difference between a stateless and stateful protocol?
A stateless protocol (like HTTP) doesn't retain any memory of previous requests — each request is independent and must contain all information needed to process it. A stateful protocol (like FTP) maintains session state across multiple requests, remembering context from earlier interactions. Web applications simulate state over stateless HTTP using cookies, sessions, or tokens (like JWT).
