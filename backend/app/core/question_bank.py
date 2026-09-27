from typing import List, Dict, Any

TECHNICAL_QUESTION_BANK: List[Dict[str, Any]] = [
    # ==================== 1. PYTHON (5 Questions) ====================
    {
        "question_id": "q_py_01",
        "domain": "Python",
        "difficulty": "INTERMEDIATE",
        "prompt": "What does the following code return when executed in Python 3?",
        "code_snippet": "def fn(vals=[]):\n    vals.append(len(vals))\n    return vals\n\nprint(fn(), fn())",
        "options": [
            "([0], [0])",
            "([0, 1], [0, 1])",
            "([0], [0, 1])",
            "Raises a TypeError"
        ],
        "correct_answer": "([0, 1], [0, 1])",
        "explanation": "Default argument expressions are evaluated once when the function definition is executed. Thus, `vals` persists across calls as a shared mutable object.",
        "skill_measured": "Python"
    },
    {
        "question_id": "q_py_02",
        "domain": "Python",
        "difficulty": "BEGINNER",
        "prompt": "Which of the following data structures in Python is immutable?",
        "code_snippet": "a = (1, 2, [3, 4])",
        "options": [
            "List",
            "Dictionary",
            "Tuple",
            "Set"
        ],
        "correct_answer": "Tuple",
        "explanation": "Tuples are immutable sequences in Python; their elements cannot be rebound or altered after instantiation.",
        "skill_measured": "Python"
    },
    {
        "question_id": "q_py_03",
        "domain": "Python",
        "difficulty": "ADVANCED",
        "prompt": "What is the primary role of the `__slots__` attribute in a Python class definition?",
        "code_snippet": "class MyClass:\n    __slots__ = ('name', 'age')",
        "options": [
            "Prevent inheritance from subclassing MyClass",
            "Suppress dynamic creation of __dict__ to optimize memory usage",
            "Enforce static typing for class properties",
            "Automatically generate getter and setter methods"
        ],
        "correct_answer": "Suppress dynamic creation of __dict__ to optimize memory usage",
        "explanation": "`__slots__` allocates a fixed amount of space for specified attributes, avoiding the creation of instance `__dict__` and significantly reducing RAM footprint.",
        "skill_measured": "Python"
    },
    {
        "question_id": "q_py_04",
        "domain": "Python",
        "difficulty": "INTERMEDIATE",
        "prompt": "What is the result of using `asyncio.gather(*tasks)` in Python async code?",
        "code_snippet": "import asyncio\nresults = await asyncio.gather(coro1(), coro2())",
        "options": [
            "Executes coroutines sequentially in a blocking thread pool",
            "Runs asynchronous awaitable objects concurrently and returns a list of results in order",
            "Creates OS-level multiprocessing workers for concurrent tasks",
            "Cancels any task taking longer than 1 second"
        ],
        "correct_answer": "Runs asynchronous awaitable objects concurrently and returns a list of results in order",
        "explanation": "`asyncio.gather` schedules given awaitables concurrently on the event loop, aggregating returned values preserving task order.",
        "skill_measured": "Python"
    },
    {
        "question_id": "q_py_05",
        "domain": "Python",
        "difficulty": "BEGINNER",
        "prompt": "What will `list(filter(lambda x: x % 2 == 0, [1, 2, 3, 4, 5]))` evaluate to?",
        "options": [
            "[1, 3, 5]",
            "[2, 4]",
            "[True, False, True, False, True]",
            "[0, 2, 4]"
        ],
        "correct_answer": "[2, 4]",
        "explanation": "`filter` retains elements for which the predicate returns `True`, extracting even integers `2` and `4`.",
        "skill_measured": "Python"
    },

    # ==================== 2. NETWORKING (5 Questions) ====================
    {
        "question_id": "q_net_01",
        "domain": "Networking",
        "difficulty": "INTERMEDIATE",
        "prompt": "Which network protocol is responsible for mapping an IP address to a hardware MAC address on a local subnet?",
        "options": [
            "DNS (Domain Name System)",
            "DHCP (Dynamic Host Configuration Protocol)",
            "ARP (Address Resolution Protocol)",
            "ICMP (Internet Control Message Protocol)"
        ],
        "correct_answer": "ARP (Address Resolution Protocol)",
        "explanation": "ARP operates at Layer 2/Layer 3 boundaries to map 32-bit IPv4 addresses to 48-bit Ethernet MAC addresses.",
        "skill_measured": "Networking"
    },
    {
        "question_id": "q_net_02",
        "domain": "Networking",
        "difficulty": "BEGINNER",
        "prompt": "At which OSI Layer does the TCP protocol operate?",
        "options": [
            "Layer 3 - Network Layer",
            "Layer 4 - Transport Layer",
            "Layer 2 - Data Link Layer",
            "Layer 7 - Application Layer"
        ],
        "correct_answer": "Layer 4 - Transport Layer",
        "explanation": "TCP and UDP are Layer 4 Transport Layer protocols providing end-to-end connection state and port multiplexing.",
        "skill_measured": "Networking"
    },
    {
        "question_id": "q_net_03",
        "domain": "Networking",
        "difficulty": "ADVANCED",
        "prompt": "In TCP 3-way handshakes, what flags are exchanged sequentially between Client and Server?",
        "options": [
            "FIN -> FIN-ACK -> ACK",
            "SYN -> SYN-ACK -> ACK",
            "RST -> SYN -> ACK",
            "CONNECT -> ACCEPT -> READY"
        ],
        "correct_answer": "SYN -> SYN-ACK -> ACK",
        "explanation": "The initiator sends SYN, responder replies with SYN-ACK, and initiator completes connection establishment with ACK.",
        "skill_measured": "Networking"
    },
    {
        "question_id": "q_net_04",
        "domain": "Networking",
        "difficulty": "INTERMEDIATE",
        "prompt": "What is the CIDR subnet mask corresponding to `/24`?",
        "options": [
            "255.255.0.0",
            "255.255.255.0",
            "255.255.255.128",
            "255.255.240.0"
        ],
        "correct_answer": "255.255.255.0",
        "explanation": "A `/24` prefix specifies 24 leading binary 1-bits, translating to `255.255.255.0` (256 host IP slots).",
        "skill_measured": "Networking"
    },
    {
        "question_id": "q_net_05",
        "domain": "Networking",
        "difficulty": "BEGINNER",
        "prompt": "Which default TCP port is used for secure HTTPS web traffic?",
        "options": [
            "80",
            "22",
            "443",
            "8080"
        ],
        "correct_answer": "443",
        "explanation": "Port 80 is unencrypted HTTP, whereas port 443 is reserved for TLS/SSL encrypted HTTPS communications.",
        "skill_measured": "Networking"
    },

    # ==================== 3. LINUX (5 Questions) ====================
    {
        "question_id": "q_lin_01",
        "domain": "Linux",
        "difficulty": "BEGINNER",
        "prompt": "Which command grants read, write, and execute permissions to file owner, and read-only to group/others?",
        "code_snippet": "chmod ??? script.sh",
        "options": [
            "chmod 744 script.sh",
            "chmod 755 script.sh",
            "chmod 644 script.sh",
            "chmod 777 script.sh"
        ],
        "correct_answer": "chmod 744 script.sh",
        "explanation": "Octal 7 represents `rwx` (4+2+1) for owner, octal 4 represents `r--` for group, and 4 for others.",
        "skill_measured": "Linux"
    },
    {
        "question_id": "q_lin_02",
        "domain": "Linux",
        "difficulty": "INTERMEDIATE",
        "prompt": "What does the `ps aux | grep python` pipeline accomplish?",
        "options": [
            "Searches file contents inside python scripts for matching strings",
            "Lists all running processes and filters for python-related process lines",
            "Installs python dependencies via PIP",
            "Terminates all active python background threads"
        ],
        "correct_answer": "Lists all running processes and filters for python-related process lines",
        "explanation": "`ps aux` lists processes across all users; piping `|` to `grep python` filters stdout for lines containing 'python'.",
        "skill_measured": "Linux"
    },
    {
        "question_id": "q_lin_03",
        "domain": "Linux",
        "difficulty": "ADVANCED",
        "prompt": "In systemd service management, what target specifies multi-user non-graphical boot state?",
        "options": [
            "graphical.target",
            "multi-user.target",
            "rescue.target",
            "default.target"
        ],
        "correct_answer": "multi-user.target",
        "explanation": "`multi-user.target` sets up standard CLI server runlevel 3 without X11 or GUI display server overhead.",
        "skill_measured": "Linux"
    },
    {
        "question_id": "q_lin_04",
        "domain": "Linux",
        "difficulty": "INTERMEDIATE",
        "prompt": "Which directory in Linux filesystem standard hierarchy contains transient system log files?",
        "options": [
            "/etc/log",
            "/var/log",
            "/usr/log",
            "/tmp/log"
        ],
        "correct_answer": "/var/log",
        "explanation": "Variable data such as system logs (`syslog`, `auth.log`, `journal`) are stored under `/var/log`.",
        "skill_measured": "Linux"
    },
    {
        "question_id": "q_lin_05",
        "domain": "Linux",
        "difficulty": "BEGINNER",
        "prompt": "Which command is used to output the current working directory absolute path?",
        "options": [
            "ls -l",
            "pwd",
            "cd .",
            "whoami"
        ],
        "correct_answer": "pwd",
        "explanation": "`pwd` stands for 'print working directory', outputting absolute path of current shell location.",
        "skill_measured": "Linux"
    },

    # ==================== 4. CYBERSECURITY (5 Questions) ====================
    {
        "question_id": "q_sec_01",
        "domain": "Cybersecurity",
        "difficulty": "INTERMEDIATE",
        "prompt": "What security vulnerability occurs when user-supplied input is directly rendered into HTML DOM without escaping?",
        "options": [
            "SQL Injection (SQLi)",
            "Cross-Site Scripting (XSS)",
            "Cross-Site Request Forgery (CSRF)",
            "Server-Side Request Forgery (SSRF)"
        ],
        "correct_answer": "Cross-Site Scripting (XSS)",
        "explanation": "XSS vulnerabilities allow attackers to execute malicious JavaScript in victim browsers when unescaped HTML input is rendered.",
        "skill_measured": "Cybersecurity"
    },
    {
        "question_id": "q_sec_02",
        "domain": "Cybersecurity",
        "difficulty": "BEGINNER",
        "prompt": "Which cryptographic hash algorithm is considered cryptographically broken and unsafe for passwords?",
        "options": [
            "Argon2id",
            "Bcrypt",
            "MD5",
            "PBKDF2"
        ],
        "correct_answer": "MD5",
        "explanation": "MD5 suffers from severe collision flaws and fast GPU cracking speeds, making it unsafe for security applications.",
        "skill_measured": "Cybersecurity"
    },
    {
        "question_id": "q_sec_03",
        "domain": "Cybersecurity",
        "difficulty": "ADVANCED",
        "prompt": "In public key cryptography (RSA/ECC), which key is used to decrypt data that was encrypted with a user's Public Key?",
        "options": [
            "Sender's Public Key",
            "Recipient's Private Key",
            "Shared Symmetric AES Key",
            "Root CA Certificate"
        ],
        "correct_answer": "Recipient's Private Key",
        "explanation": "In asymmetric encryption, messages encrypted with a public key can ONLY be decrypted by the corresponding secret private key.",
        "skill_measured": "Cybersecurity"
    },
    {
        "question_id": "q_sec_04",
        "domain": "Cybersecurity",
        "difficulty": "INTERMEDIATE",
        "prompt": "Which security control prevents malicious cross-origin requests by instructing browsers which domains can load resources?",
        "options": [
            "CORS (Cross-Origin Resource Sharing)",
            "CSP (Content Security Policy)",
            "HSTS (HTTP Strict Transport Security)",
            "X-Frame-Options"
        ],
        "correct_answer": "CSP (Content Security Policy)",
        "explanation": "CSP HTTP headers restrict executable scripts, inline styles, and external origins to mitigate XSS and data injection attacks.",
        "skill_measured": "Cybersecurity"
    },
    {
        "question_id": "q_sec_05",
        "domain": "Cybersecurity",
        "difficulty": "BEGINNER",
        "prompt": "What is the primary objective of Multi-Factor Authentication (MFA)?",
        "options": [
            "Encrypt database disk storage at rest",
            "Require two or more distinct evidence factors (knowledge, possession, inherence) before granting access",
            "Automatically rotate API keys every 24 hours",
            "Block IP addresses sending more than 100 requests per second"
        ],
        "correct_answer": "Require two or more distinct evidence factors (knowledge, possession, inherence) before granting access",
        "explanation": "MFA strengthens identity verification by combining independent factors (e.g. password + TOTP authenticator token).",
        "skill_measured": "Cybersecurity"
    },

    # ==================== 5. AI / MACHINE LEARNING (5 Questions) ====================
    {
        "question_id": "q_ai_01",
        "domain": "AI / Machine Learning",
        "difficulty": "INTERMEDIATE",
        "prompt": "In recommendation systems, what does Cosine Similarity compute between two vector representations $A$ and $B$?",
        "options": [
            "The Euclidean distance between vector endpoints",
            "The cosine of the angle between two non-zero vectors in inner product space: $\\frac{A \\cdot B}{\\|A\\| \\|B\\|}$",
            "The Jaccard index of overlapping category strings",
            "The Pearson correlation matrix eigenvalue"
        ],
        "correct_answer": "The cosine of the angle between two non-zero vectors in inner product space: $\\frac{A \\cdot B}{\\|A\\| \\|B\\|}$",
        "explanation": "Cosine similarity measures directional orientation irrespective of vector magnitude, returning values between -1 and 1.",
        "skill_measured": "AI / Machine Learning"
    },
    {
        "question_id": "q_ai_02",
        "domain": "AI / Machine Learning",
        "difficulty": "BEGINNER",
        "prompt": "What technique converts variable-length text documents into numerical term importance matrix representation?",
        "options": [
            "TF-IDF (Term Frequency-Inverse Document Frequency)",
            "K-Means Clustering",
            "Principal Component Analysis",
            "Gradient Descent Optimizer"
        ],
        "correct_answer": "TF-IDF (Term Frequency-Inverse Document Frequency)",
        "explanation": "TF-IDF evaluates how relevant a word is to a document in a collection by weighting local frequency against global corpus occurrence.",
        "skill_measured": "AI / Machine Learning"
    },
    {
        "question_id": "q_ai_03",
        "domain": "AI / Machine Learning",
        "difficulty": "ADVANCED",
        "prompt": "What failure mode occurs during neural network training when gradients shrink exponentially towards zero during backpropagation?",
        "options": [
            "Exploding Gradient Problem",
            "Vanishing Gradient Problem",
            "Catastrophic Forgetting",
            "Mode Collapse"
        ],
        "correct_answer": "Vanishing Gradient Problem",
        "explanation": "Saturating activations (like sigmoid or tanh) in deep architectures multiply small partial derivatives, causing early layer weights to stop updating.",
        "skill_measured": "AI / Machine Learning"
    },
    {
        "question_id": "q_ai_04",
        "domain": "AI / Machine Learning",
        "difficulty": "INTERMEDIATE",
        "prompt": "Which evaluation metric measures the ratio of true positive predictions to all positive predictions made by a classifier?",
        "options": [
            "Recall",
            "Precision",
            "F1-Score",
            "ROC-AUC"
        ],
        "correct_answer": "Precision",
        "explanation": "Precision = TP / (TP + FP), indicating the exactness of positive class predictions.",
        "skill_measured": "AI / Machine Learning"
    },
    {
        "question_id": "q_ai_05",
        "domain": "AI / Machine Learning",
        "difficulty": "BEGINNER",
        "prompt": "What is the primary risk of training a machine learning model for too many epochs on a small dataset?",
        "options": [
            "Underfitting",
            "Overfitting",
            "High bias",
            "Feature dilution"
        ],
        "correct_answer": "Overfitting",
        "explanation": "Overfitting occurs when a model memorizes dataset noise instead of learning generalizable representations.",
        "skill_measured": "AI / Machine Learning"
    },

    # ==================== 6. SQL (5 Questions) ====================
    {
        "question_id": "q_sql_01",
        "domain": "SQL",
        "difficulty": "INTERMEDIATE",
        "prompt": "Which SQL clause is used to filter aggregated group data resulting from a `GROUP BY` clause?",
        "options": [
            "WHERE",
            "HAVING",
            "ORDER BY",
            "FILTER"
        ],
        "correct_answer": "HAVING",
        "explanation": "`WHERE` filters individual rows prior to grouping, whereas `HAVING` filters aggregated records after `GROUP BY` execution.",
        "skill_measured": "SQL"
    },
    {
        "question_id": "q_sql_02",
        "domain": "SQL",
        "difficulty": "BEGINNER",
        "prompt": "What JOIN type returns all records from the left table and matching records from the right table?",
        "options": [
            "INNER JOIN",
            "LEFT JOIN",
            "RIGHT JOIN",
            "FULL OUTER JOIN"
        ],
        "correct_answer": "LEFT JOIN",
        "explanation": "`LEFT JOIN` guarantees all rows from the left table appear in result set, filling unmatched right columns with `NULL`.",
        "skill_measured": "SQL"
    },
    {
        "question_id": "q_sql_03",
        "domain": "SQL",
        "difficulty": "ADVANCED",
        "prompt": "In PostgreSQL, what window function assigns a sequential integer rank without gaps when ties occur?",
        "code_snippet": "SELECT DENSE_RANK() OVER (ORDER BY score DESC) FROM quiz_results;",
        "options": [
            "ROW_NUMBER()",
            "RANK()",
            "DENSE_RANK()",
            "NTILE(4)"
        ],
        "correct_answer": "DENSE_RANK()",
        "explanation": "`DENSE_RANK()` leaves no numeric gaps after tied values (e.g. 1, 2, 2, 3), whereas `RANK()` skips ranks (1, 2, 2, 4).",
        "skill_measured": "SQL"
    },
    {
        "question_id": "q_sql_04",
        "domain": "SQL",
        "difficulty": "INTERMEDIATE",
        "prompt": "What type of index in PostgreSQL optimizes full-text text search queries?",
        "options": [
            "B-Tree Index",
            "GIN (Generalized Inverted Index)",
            "BRIN (Block Range Index)",
            "Hash Index"
        ],
        "correct_answer": "GIN (Generalized Inverted Index)",
        "explanation": "GIN indexes map internal words to matching row pointers, accelerating full-text `tsvector` queries and JSONB array lookups.",
        "skill_measured": "SQL"
    },
    {
        "question_id": "q_sql_05",
        "domain": "SQL",
        "difficulty": "BEGINNER",
        "prompt": "Which SQL statement adds a new column `last_evaluated` to an existing `user_skills` table?",
        "options": [
            "UPDATE TABLE user_skills ADD COLUMN last_evaluated TIMESTAMP;",
            "ALTER TABLE user_skills ADD COLUMN last_evaluated TIMESTAMPTZ;",
            "MODIFY TABLE user_skills INSERT COLUMN last_evaluated TIMESTAMP;",
            "CREATE COLUMN last_evaluated ON user_skills;"
        ],
        "correct_answer": "ALTER TABLE user_skills ADD COLUMN last_evaluated TIMESTAMPTZ;",
        "explanation": "`ALTER TABLE` is DDL command used to modify existing table structures by adding or dropping columns.",
        "skill_measured": "SQL"
    },

    # ==================== 7. WEB DEVELOPMENT (5 Questions) ====================
    {
        "question_id": "q_web_01",
        "domain": "Web Development",
        "difficulty": "INTERMEDIATE",
        "prompt": "In React 18, what hook is used to persist mutable reference values across renders without triggering a re-render?",
        "options": [
            "useState",
            "useMemo",
            "useRef",
            "useCallback"
        ],
        "correct_answer": "useRef",
        "explanation": "`useRef` returns a mutable ref object whose `.current` property persists across re-renders without causing component re-evaluation.",
        "skill_measured": "Web Development"
    },
    {
        "question_id": "q_web_02",
        "domain": "Web Development",
        "difficulty": "BEGINNER",
        "prompt": "Which HTTP request method should be used for idempotent updates to a resource endpoint?",
        "options": [
            "POST",
            "PUT",
            "CONNECT",
            "TRACE"
        ],
        "correct_answer": "PUT",
        "explanation": "`PUT` is idempotent according to RFC 7231; calling it multiple times with identical payload produces identical server state.",
        "skill_measured": "Web Development"
    },
    {
        "question_id": "q_web_03",
        "domain": "Web Development",
        "difficulty": "ADVANCED",
        "prompt": "What browser mechanism isolates execution contexts between different origin iframe documents?",
        "options": [
            "Event Loop Microtask Queue",
            "Same-Origin Policy (SOP)",
            "Web Worker Thread Pool",
            "Service Worker Cache API"
        ],
        "correct_answer": "Same-Origin Policy (SOP)",
        "explanation": "SOP prevents scripts on one origin from accessing DOM or cookies of another origin unless explicit CORS headers permit.",
        "skill_measured": "Web Development"
    },
    {
        "question_id": "q_web_04",
        "domain": "Web Development",
        "difficulty": "INTERMEDIATE",
        "prompt": "In TypeScript, what type keyword creates a new type containing a subset of properties picked from T?",
        "code_snippet": "type UserPreview = Pick<User, 'id' | 'name'>;",
        "options": [
            "Omit<T, K>",
            "Pick<T, K>",
            "Partial<T>",
            "Extract<T, U>"
        ],
        "correct_answer": "Pick<T, K>",
        "explanation": "`Pick<T, K>` constructs a type by choosing specified keys `K` from interface `T`.",
        "skill_measured": "Web Development"
    },
    {
        "question_id": "q_web_05",
        "domain": "Web Development",
        "difficulty": "BEGINNER",
        "prompt": "Which CSS flexbox property aligns items along the cross axis inside a flex container?",
        "options": [
            "justify-content",
            "align-items",
            "flex-direction",
            "align-content"
        ],
        "correct_answer": "align-items",
        "explanation": "`justify-content` manages main-axis alignment, whereas `align-items` controls perpendicular cross-axis alignment.",
        "skill_measured": "Web Development"
    },

    # ==================== 8. CLOUD COMPUTING (5 Questions) ====================
    {
        "question_id": "q_cld_01",
        "domain": "Cloud Computing",
        "difficulty": "INTERMEDIATE",
        "prompt": "In Docker containerization, what instruction specifies the base image layer in a Dockerfile?",
        "code_snippet": "FROM python:3.11-slim",
        "options": [
            "RUN",
            "FROM",
            "ENTRYPOINT",
            "EXPOSE"
        ],
        "correct_answer": "FROM",
        "explanation": "`FROM` initializes a new build stage and sets the foundational base image for subsequent Dockerfile instructions.",
        "skill_measured": "Cloud Computing"
    },
    {
        "question_id": "q_cld_02",
        "domain": "Cloud Computing",
        "difficulty": "BEGINNER",
        "prompt": "What type of cloud deployment architecture runs application code dynamically on demand without persistent server management?",
        "options": [
            "Bare-metal Hypervisor",
            "Serverless / FaaS (Function-as-a-Service)",
            "IaaS Virtual Machine Pool",
            "Monolithic Container Host"
        ],
        "correct_answer": "Serverless / FaaS (Function-as-a-Service)",
        "explanation": "Serverless models execute functions in response to events, scaling to zero when idle and abstracting server infrastructure.",
        "skill_measured": "Cloud Computing"
    },
    {
        "question_id": "q_cld_03",
        "domain": "Cloud Computing",
        "difficulty": "ADVANCED",
        "prompt": "In Kubernetes architecture, what master node component maintains cluster state in a distributed key-value store?",
        "options": [
            "kube-scheduler",
            "kube-apiserver",
            "etcd",
            "kubelet"
        ],
        "correct_answer": "etcd",
        "explanation": "`etcd` is a strongly consistent, distributed key-value store holding the complete declarative state of a Kubernetes cluster.",
        "skill_measured": "Cloud Computing"
    },
    {
        "question_id": "q_cld_04",
        "domain": "Cloud Computing",
        "difficulty": "INTERMEDIATE",
        "prompt": "Which AWS/Cloud service model allows automated provisioning of infrastructure resources using declarative code files?",
        "options": [
            "Infrastructure as Code (IaC)",
            "Platform as a Service (PaaS)",
            "Software as a Service (SaaS)",
            "Storage as a Service (STaaS)"
        ],
        "correct_answer": "Infrastructure as Code (IaC)",
        "explanation": "IaC tools (Terraform, CloudFormation) manage cloud resources reproducibly via version-controlled configuration manifests.",
        "skill_measured": "Cloud Computing"
    },
    {
        "question_id": "q_cld_05",
        "domain": "Cloud Computing",
        "difficulty": "BEGINNER",
        "prompt": "What cloud computing service category provides operating system runtimes, databases, and middleware as a service?",
        "options": [
            "IaaS (Infrastructure as a Service)",
            "PaaS (Platform as a Service)",
            "SaaS (Software as a Service)",
            "DaaS (Desktop as a Service)"
        ],
        "correct_answer": "PaaS (Platform as a Service)",
        "explanation": "PaaS delivers managed runtime environments allowing developers to deploy applications without managing underlying VMs or OS patches.",
        "skill_measured": "Cloud Computing"
    }
]
