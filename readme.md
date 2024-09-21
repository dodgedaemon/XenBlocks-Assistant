# Vast.ai XenBlocks Mining Assistant - Woody Edition

Welcome to **TreeCityWes.eth's** Vast.ai XenBlocks Mining Assistant - Woody Edition! This Python tool optimizes XenBlocks X1 mining on Vast.ai, helping you monitor instance stats, terminate non-profitable instances, and discover new lucrative offers. It now integrates **WoodyMiner**, providing advanced miner statistics and support.

Sign up for Vast Cloud GPU Rental here: [Vast.ai Sign-Up](https://cloud.vast.ai/?ref_id=130895).

## Features

- **Monitor Instance Stats:** Automatically fetch and display key metrics from your mining instances using both Vast.ai and **WoodyMiner** integration.
- **Kill Dead Instances:** Identify and terminate unprofitable instances, cutting unnecessary expenses.
- **Find New Offers:** Use advanced filtering to uncover the most cost-effective mining opportunities on Vast.ai.

## Getting Started

### Prerequisites

- Python 3.6 or later.
- A Vast.ai API key and wallet address configured via an `.env` file for secure access.
- Funded Vast.ai Account 
### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/TreeCityWes/XenBlocks-Assistant.git
   cd XenBlocks-Assistant
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install --upgrade vastai
   vastai set api-key (your API key)
   ```

   ![image](https://github.com/TreeCityWes/XenBlocks-Assistant/assets/93751858/bdfb2499-0cd7-405a-a552-a0330c6690cc)

3. **Configure .ENV File:**

   Create a `.env` file in the root directory of the project with your Vast.ai API key and wallet address.

   This file should contain the following lines:
   ```
   API_KEY=your_vast_ai_api_key
   ADDR=your_wallet_address
   ```

   Replace `your_vast_ai_api_key` and `your_wallet_address` with the actual values you wish to use for mining.

### Usage

Run the script from the command line:
```bash
python vastmon-woody.py
```

### Support

For support, visit [HashHead.io](https://hashhead.io)

Or Buy Us A Coffee! 
- Woody: [woodysoil.com](https://woodysoil.com)
- Smit: [buymeacoffee.com/smit1237](https://buymeacoffee.com/smit1237)
- Wes: [buymeacoffee.com/treecitywes](https://buymeacoffee.com/treecitywes)

