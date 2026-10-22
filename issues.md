# Static Code Analysis Issues and Fixes

| Issue | Type | Line(s) | Description | Fix Approach |
| :--- | :--- | :--- | :--- | :--- |
| **B301 / B402 (Unsafe Deserialization)** | Security (Bandit) | 52, 59 | Use of `marshal.dumps` / `marshal.loads` allows arbitrary code execution and binary instability. | Replaced `marshal` binary serialization with safe, human-readable `json` serialization (`json.dump` / `json.load`). |
| **B105 (Hardcoded Password)** | Security (Bandit) | 62 | Hardcoded FTP plain-text password `Bureau#2024` in `uploadToBureau`. | Removed insecure remote FTP module and hardcoded credentials. |
| **B603 / B607 (Insecure Subprocess Call)** | Security (Bandit) | 69 | Calling external `mail` shell utility via `subprocess.run` without binary validation. | Removed shell-dependent subprocess call in favor of direct logging. |
| **Logical Calculation Bug (EMI Rate)** | Logic Bug | 14, 91 | Annual interest rate passed directly as percentage (e.g., `9`) causing EMI calculation to yield absurd values (~375,000/month for a 5L loan). | Converted percentage input to decimal rate (`(annual_rate / 100) / 12`). |
| **W0102 (Mutable Default Argument)** | Quality (Pylint) | 18 | `history=[]` shares a mutable list across function calls. | Changed parameter default to `None` and initialized `history = []` inside body. |
| **C0103 (Naming Style Violation)** | Quality (Pylint) | Multiple | Function names used `camelCase` (`calculateEMI`, `checkEligibility`) instead of `snake_case`. | Renamed all functions and variables to comply with PEP 8 `snake_case`. |
| **E501 (Line Length Exceeded)** | Style (Flake8) | 73, 91 | Lines exceeded maximum allowed 79 characters. | Wrapped parameters across multiple lines. |