/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */

// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  // Hide sidebar that's home page
  // tutorialSidebar: [{type: 'doc', id: 'index'}],

  overviewSidebar: [
    {
      type: "category",
      label: "Overview",
      items: [
        "overview/introduction",
        "overview/overview",
        "overview/key-features",
        "overview/consensus",
        "overview/whitepaper",
        "overview/disclaimer",
      ],
    },
  ],
  learnSidebar: [
    "learn/overview",
    "learn/glossary",
    {
      type: "category",
      label: "Basics",
      items: ["learn/nodes", "learn/spectrum", "learn/tokenomics"],
    },
    {
      type: "category",
      label: "Governance",
      items: [
        "learn/governance",
        "learn/quorum",
        "learn/arbitrator",
        "learn/proposals",
        "learn/decision-making",
        "learn/dispute-resolution",
        "learn/updates-changes",
      ],
    },
    {
      type: "category",
      label: "Mining",
      items: ["learn/upow", "learn/hw", "learn/sw", "learn/pool"],
    },
    {
      type: "category",
      label: "Smart Contracts and IPOs",
      items: [
        "learn/smart-contracts",
        "learn/ipo",
        "learn/dutch-auction",
        "learn/qouterry",
        "learn/qx",
        "learn/random",
        "learn/mlm",
      ],
    },
    "learn/aigarth",
    {
      type: "category",
      label: "How to buy",
      items: ["learn/invest", "learn/wallets", "learn/qx"],
    },
  ],

  compSidebar: [
    {
      type: "category",
      label: "Getting Started",
      items: [
        "computors/challenges",
        "computors/prerequisites",
        "computors/installation",
        "computors/configuration",
      ],
    },
    {
      type: "category",
      label: "Run a Computor",
      items: ["computors/bm", "computors/vm"],
    },
    {
      type: "category",
      label: "Monitoring & Maintenance",
      items: [
        "computors/logging",
        "computors/commands",
        "computors/backup-restore",
        "computors/upgrading",
      ],
    },
  ],
  devSidebar: [
    "developers/intro", // Entry point explaining the paths
    {
      type: "category",
      label: "Smart Contracts", // Comprehensive SC section
      items: [
        "developers/smart-contracts/overview",
        {
          type: "category",
          label: "Getting Started",
          items: [
            "developers/dev-kit", // Enhanced setup guide
            "developers/smart-contracts/getting-started/setup-enviroment",
            "developers/smart-contracts/getting-started/add-your-contract",
            "developers/smart-contracts/getting-started/test-your-contract",
            "developers/smart-contracts/getting-started/congratulations",
          ],
        },
        {
          type: "category",
          label: "Contract Development",
          items: [
            "developers/qpi", // Enhanced QPI guide
            "developers/smart-contracts/smart-contract/overview",
            "developers/smart-contracts/smart-contract/contract-structure",
            "developers/smart-contracts/smart-contract/data-types",
            "developers/smart-contracts/smart-contract/procedures-and-functions",
            "developers/smart-contracts/smart-contract/states",
            "developers/smart-contracts/smart-contract/cross-inner-call",
            "developers/smart-contracts/smart-contract/assets-and-shares",
            "developers/smart-contracts/smart-contract/how-sc-actually-work",
            "developers/smart-contracts/smart-contract/code-style",
            "developers/smart-contracts/smart-contract/programs-in-practice",
            "developers/smart-contracts/smart-contract/restrictions",
          ],
        },
        {
          type: "category",
          label: "CLI Tools",
          items: [
            "developers/smart-contracts/cli/Overview",
            "developers/smart-contracts/cli/call-contract-function",
            "developers/smart-contracts/cli/invoke-contract-procedure",
          ],
        },
        {
          type: "category",
          label: "Examples",
          items: [
            "developers/smart-contracts/sc-by-examples/assets-and-shares",
            "developers/smart-contracts/sc-by-examples/qns",
          ],
        },
        {
          type: "category",
          label: "Testing",
          items: [
            "developers/testnet-resources", // Enhanced testing resources
            "developers/smart-contracts/testing/overview",
            "developers/smart-contracts/testing/contract-testing",
            "developers/smart-contracts/testing/testnet",
          ],
        },
        {
          type: "category",
          label: "Resources",
          items: [
            "developers/oracles", // Advanced SC concept
            "developers/smart-contracts/resources/contract-verify-tool",
            "developers/smart-contracts/resources/qubic-lite-core",
          ],
        },
        "developers/dev-kit", // Setup
        "developers/testnet-resources", // Testing Env
        "developers/qpi", // Core Language/Interface
        "developers/oracles", // Advanced SC concept
      ],
    },
    {
      type: "category",
      label: "Frontend & Interaction", // Path 2 & 3 combined
      items: [
        "api/rpc", // Connecting (Included directly)
        "api/wallet-integrations", // Wallets (Moved from apiSidebar)
        "developers/frontend-integration", // Guide for interaction
        {
          type: "category",
          label: "RPC Integration", // Enhanced RPC section
          items: [
            "developers/smart-contracts/rpc/Overview",
            "developers/smart-contracts/rpc/setup-rpc",
            "developers/smart-contracts/rpc/ts-library",
          ],
        },
        {
          type: "category",
          label: "Libraries", // Key tools for this path
          items: [
            "developers/library-typescript",
            "developers/library-java",
            "developers/library-go",
            "developers/library-http",
            "developers/library-csharp",
            "developers/library-rust",
          ],
        },
        {
          type: "category",
          label: "External Services", // Third-party integrations
          items: [
            "developers/exolix-integration", // Exolix exchange integration
          ],
        },
      ],
    },
    {
      type: "category",
      label: "3. Developer Guide",
      items: [
        "developers/ticks-and-concurrency",
        "developers/smart-contract-architecture",
      ],
    },
    {
      type: "category",
      label: "4. Tools & Clients", // General tools
      items: [
        "developers/qubic-node",
        "developers/qubic-cli",
        "developers/client-qubicj-shell",
      ],
    },
    {
      type: "category",
      label: "5. Community & Programs", // Other resources
      items: [
        "developers/contribute",
        "developers/grants",
        "developers/bug-bounty",
      ],
    },
    {
      type: "category",
      label: "6. Tutorials", // Keep tutorials separate for now
      items: ["developers/tutorials"],
    },
  ],
  apiSidebar: [
    {
      type: "category",
      label: "API Reference",
      items: [
        "api/rpc", // Keep the pure RPC reference here
      ],
    },
  ],
};

module.exports = sidebars;
