/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  learnSidebar: [
    {
      type: 'category',
      label: 'Basics',
      items: [
        'learn/basics/overview',
        'learn/basics/Glossary',
        'learn/basics/Tokenomics',
        'learn/basics/Node Types',
        'learn/basics/Spectrum',
        'learn/basics/Qubic Architecture',
      ],
    },
    {
      type: 'category',
      label: 'Governance',
      items: [
        'learn/governance/Separation of Power',
        'learn/governance/Quorum',
        'learn/governance/Arbitrator',
        'learn/governance/Steering Committee',
        'learn/governance/Proposals',
        'learn/governance/Decision Making',
        'learn/governance/Dispute Resolution',
        'learn/governance/Updates and Changes',
      ],
    },
    {
      type: 'category',
      label: 'Mining',
      items: [
        'learn/mining/Usefull Proof of Work',
        'learn/mining/Mining Hardware',
        'learn/mining/Mining Software',
        'learn/mining/Joining a Pool',
      ],
    },
    {
      type: 'category',
      label: 'Advanced Concepts',
      items: [
        'learn/advanced concepts/Smart Contracts',
        'learn/advanced concepts/IPO',
        'learn/advanced concepts/Dutch Auction',
        'learn/advanced concepts/Aigarth',
        'learn/advanced concepts/Oracles',
        'learn/advanced concepts/Environmental Impact',
      ],
    },
    {
      type: 'category',
      label: 'User Guide',
      items: [
        'learn/user guide/Invest in Qubic',
        'learn/user guide/Wallets',
        'learn/user guide/Exchanges',
        'learn/user guide/Qx (DEX)',
      ],
    },
    {
      type: 'category',
      label: 'Ecosystem',
      items: [
        'learn/ecosystem/Use Cases',
        'learn/ecosystem/Community Engagement',
        'learn/ecosystem/Grants Program',
        'learn/ecosystem/Hackathons',
        'learn/ecosystem/Valis Project',
      ],
    },
    {
      type: 'category',
      label: 'Roadmap',
      items: [
        'learn/roadmap/Project Milestones',
        'learn/roadmap/Upcoming Features',
        'learn/roadmap/Release History',
        'learn/roadmap/Project X',
      ],
    },
    'learn/Security',
  ],
  
  overviewSidebar: [
    'overview/Introduction',
    'overview/Key Features',
    'overview/Qubic Consensus',
    'overview/Team and Founder',
    'overview/Future Developments',
    'overview/Community and Adoption',
    'overview/Disclaimer',
  ],

  compSidebar: [
    {
      type: 'category',
      label: 'Getting Started',
      items: [
        'computors/challenges',
        'computors/prerequisites',
        'computors/installation',
        'computors/configuration',
      ],
    },
    {
      type: 'category',
      label: 'Run a Computor',
      items: [
        'computors/bm',
        'computors/vm',
      ],
    },
    {
      type: 'category',
      label: 'Monitoring & Maintenance',
      items: [
        'computors/logging',
        'computors/commands',
        'computors/backup-restore',
        'computors/upgrading',
      ],
    },
  ],

  devSidebar: [
    'developers/intro',
    'developers/contribute',
    {
      type: 'category',
      label: 'Core Concepts',
      items: [
        'developers/qubic-id',
        'developers/transactions',
      ],
    },
    {
      type: 'category',
      label: 'Advanced Concepts',
      items: [
        'developers/oracles',
        'developers/qpi',
      ],
    },
    {
      type: 'category',
      label: 'Clients',
      items: [
        'api/rpc',
        'developers/rust-api',
      ],
    },
    {
      type: 'category',
      label: 'Community Bounties',
      items: [
        'developers/draft/logo',
      ],
    },
    {
      type: 'category',
      label: 'Implemented Proposals',
      items: [
        'developers/empty',
      ],
    },
    {
      type: 'category',
      label: 'Tutorials',
      items: [
        'developers/environment',
      ],
    },
    'developers/bug-bounty',
  ],

  apiSidebar: [
    {
      type: 'category',
      label: 'Core API',
      items: [
        'api/rpc',
        'api/transactions',
      ],
    },
  ],
};

module.exports = sidebars;