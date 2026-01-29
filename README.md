# HTTPayer Python SDK Examples

Quickstart examples and tutorials for using the [HTTPayer Python SDK](https://pypi.org/project/httpayer/) to make x402 payment-gated API calls.

**HTTPayer** enables cross-chain stablecoin payments for APIs, AI agents, and smart contracts using the HTTP 402 Payment Required standard.

---

## Table of Contents

- [What is HTTPayer?](#what-is-httpayer)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Project Structure](#project-structure)
- [Usage](#usage)
  - [Running Jupyter Notebooks](#running-jupyter-notebooks)
  - [Running Python Scripts](#running-python-scripts)
- [Examples](#examples)
- [Resources](#resources)

---

## What is HTTPayer?

HTTPayer is a cross-chain payment system that allows you to:

- **Pay for APIs with USDC** across multiple blockchains (Base, SKALE Base, Solana)
- **Use the x402 protocol** (HTTP 402 Payment Required) for automated payments
- **Access premium APIs** like Gloria AI, Nansen, and Heurist with automatic payment handling
- **Build AI agents** that can autonomously pay for data and services

This repository contains hands-on examples to get you started quickly.

---

## Prerequisites

Before getting started, ensure you have:

- **Python 3.10+** installed ([download here](https://www.python.org/downloads/))
- **Git** installed (optional, for cloning the repository)

**For Relay Mode examples** (web3 payments):
- An EVM or Solana wallet with a private key (e.g., MetaMask, Phantom)
- USDC on Base, SKALE Base, or Solana

**For Proxy Mode examples** (API key payments):
- HTTPayer API key with credits (no web3 wallet needed)

---

## Installation

### 1. Clone or Download This Repository

```bash
git clone https://github.com/httpayer/python-sdk-examples.git
cd python-sdk-examples
```

Or download and extract the ZIP file from GitHub.

---

### 2. Install `uv` (Python Package Manager)

HTTPayer uses [uv](https://github.com/astral-sh/uv) for fast dependency management.

#### **Windows (PowerShell)**

```powershell
pip install uv
```

#### **macOS / Linux**

```bash
pip3 install uv
```

> **Note**: If you encounter permission issues, use `pip install --user uv` or `sudo pip3 install uv`.

---

### 3. Create Virtual Environment and Install Dependencies

Run this from the **root directory** of `python-sdk-examples/`:

```bash
uv sync
```

This will:

- Create a `.venv/` virtual environment
- Install all dependencies from `pyproject.toml` and `uv.lock`
- Set up Jupyter and the HTTPayer SDK

---

### 4. Configure Your Environment

Create a `.env` file in the **root directory** (`python-sdk-examples/`) with your credentials.

#### **Windows (PowerShell)**

```powershell
Copy-Item .env.sample .env
```

#### **Windows (CMD)**

```cmd
copy .env.sample .env
```

#### **macOS / Linux**

```bash
cp .env.sample .env
```

Then edit the `.env` file and add your credentials:

**For Relay Mode examples** (web3 payments):
```env
EVM_PRIVATE_KEY=your_evm_private_key_here
SOLANA_PRIVATE_KEY=your_solana_private_key_here
```
Note: Only one key is required, it can be either Solana or EVM private key.

**For Proxy Mode examples** (API key payments):
```env
HTTPAYER_API_KEY=your_api_key_here
```

> **Security Warning**: Never commit your `.env` file to version control. It's already in `.gitignore`.

---

## Project Structure

```
python-sdk-examples/
├── notebooks/              # Jupyter notebook examples
│   ├── relay_quickstart.ipynb   # Complete relay example (Gloria AI + Nansen + Heurist)
│   ├── proxy/              # Proxy mode examples (coming soon)
│   └── relay/              # Additional relay examples (coming soon)
├── scripts/                # Python script examples
│   ├── proxy/              # Proxy mode scripts
│   └── relay/              # Relay mode scripts
├── .env.sample             # Environment variable template
├── .gitignore              # Git ignore rules
├── pyproject.toml          # Project dependencies
├── uv.lock                 # Locked dependency versions
└── README.md               # This file
```

---

## Usage

### Running Jupyter Notebooks

1. **Start Jupyter**

If you plan to use Jupyter notebooks, run the following command from the project root:

```bash
# Using uv
uv run --with jupyter jupyter lab
```

2. **Open a notebook** (e.g., `notebooks/relay_quickstart.ipynb`)

3. **Select the kernel**:

   - If not already selected, click **Kernel → Change Kernel → Python 3*
   - This ensures the notebook uses the correct Python environment

4. **Run the cells** to execute the examples!

---

### Running Python Scripts

1. **Run a script**:

   ```bash
   uv run python scripts/relay/example.py
   ```

2. **Check the output** to see payment transactions and API responses.

---

## Examples

### 1. Relay Quickstart Notebook (`notebooks/relay_quickstart.ipynb`)

A comprehensive Jupyter notebook example that demonstrates:

- Initializing the HTTPayer client with your private key
- Checking relay limits (daily spending limits)
- Making x402 API calls with automatic payment handling
- Extracting payment information from response headers
- Chaining multiple API calls:
  1. Gloria AI - Fetch AI and crypto news
  2. Nansen - Get smart money netflow data
  3. Heurist AI - Search for related market analysis
  4. HTTPayer LLM - Generate investment insights

**What you'll learn**:

- How to use relay mode (HTTPayer pays the API, you pay HTTPayer)
- How to decode payment transaction hashes
- How to combine multiple data sources for AI-powered insights

---

### 2. Multi-API Orchestration Script (`scripts/relay/script.py`)

A standalone Python script demonstrating the same multi-API workflow as the notebook:

- Gloria AI news fetching
- Nansen smart money netflow analysis
- Heurist AI web search
- LLM-powered investment analysis

**What you'll learn**:

- How to structure a production-ready script with HTTPayer
- Payment extraction and decoding from response headers
- Error handling for multi-step API workflows

**Features**:

- Automatic payment handling across 4 different APIs
- Structured logging of transactions and responses
- Payment summary at completion

---

### 3. Proxy Mode Examples (`scripts/proxy/`)

Pay for x402 APIs using an API key / account system instead of a web3 wallet.

**Coming soon!**

---

## Key Concepts

### **Relay Mode vs Proxy Mode**

| Feature                     | Relay Mode                           | Proxy Mode                                    |
| --------------------------- | ------------------------------------ | --------------------------------------------- |
| **Payment Method**          | Web3 wallet (USDC on-chain)          | API key / Account system                      |
| **Web3 Wallet Required**    | Yes                                  | No                                            |
| **Payment Flow**            | You → HTTPayer → API (on-chain)      | Traditional API key authentication            |
| **Use Case**                | Cross-chain & privacy-preserving payments  | Traditional web apps, no crypto setup needed  |

### **Payment Headers**

HTTPayer responses include:

- `x-client-payment`: Your transaction hash (paying HTTPayer)
- `x-payment-response`: HTTPayer's transaction hash (paying the API)

These can be verified on blockchain explorers.

---

## Resources

- **HTTPayer Documentation**: [https://docs.httpayer.com](https://docs.httpayer.com)
- **Python SDK (PyPI)**: [https://pypi.org/project/httpayer/](https://pypi.org/project/httpayer/)
- **x402 Protocol**: [https://github.com/coinbase/x402](https://github.com/coinbase/x402)

---

## Troubleshooting

### **Issue: `ModuleNotFoundError: No module named 'httpayer'`**

**Solution**: Make sure you've synced the virtual environment with `uv sync`:

```bash
uv sync
```

---

### **Issue: `ValueError: EVM_PRIVATE_KEY environment variable is not set`**

**Solution**: Ensure you have:

1. Created a `.env` file in the root directory
2. Added your private key: `EVM_PRIVATE_KEY=your_key_here`
3. Restarted Jupyter or your Python script

---

### **Issue: `uv` command not found**

**Solution**: Install `uv` globally:

```bash
# Windows
pip install uv

# macOS/Linux
pip3 install uv
```

If it's still not found, add Python's scripts directory to your PATH.

---

## License

See [LICENSE](LICENSE) file for details.

---

## Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/httpayer/python-sdk-examples/issues)
- **Documentation**: [https://docs.httpayer.com](https://docs.httpayer.com)
- **Discord**: Join our community (link coming soon!)

---

**Happy building with HTTPayer!**
