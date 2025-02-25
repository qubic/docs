// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require('prism-react-renderer').themes.github;
const darkCodeTheme = require('prism-react-renderer').themes.dracula;

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Qubic Docs',
  tagline: 'Learn everything about Qubic you need to know.',
  favicon: 'img/qubic.ico',

  // Set the production url of your site here
  url: 'https://docs.qubic.org',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'qubic', // Usually your GitHub org/user name.
  projectName: 'docs.qubic.org', // Usually your repo name.
  scripts: [
    {
      src: "https://dashboard.letmeexplain.ai/embed/lme_chatbot_widget.js", // LetMeExplain embed script
      async: false,
    },
    {
      src: "/js/enable_lme_chatbot.js", // Custom initialization script
      defer: true,
    },
  ],
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          routeBasePath: '/', // Serve docs at the root
          path: 'docs',
          // Remove this to remove the "edit this page" links.
          // editUrl: 'https://github.com/qubic/docs',
        },
        blog: false, // Disable the blog plugin
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: 'img/qubic-docs-logo-lightmode.svg',
      navbar: {
        title: '',
        logo: {
          alt: 'Qubic Logo',
          src: 'img/qubic-docs-logo-lightmode.svg',
          srcDark: 'img/qubic-docs-logo-darkmode.svg',
        },
        items: [
          {
            label: 'Overview',
            type: 'docSidebar',
            sidebarId: 'overviewSidebar',
            position: 'left',
          },
          {
            label: 'Learn',
            type: 'docSidebar',
            sidebarId: 'learnSidebar',
            position: 'left',
          },
          {
            label: 'Computors',
            type: 'docSidebar',
            sidebarId: 'compSidebar',
            position: 'left',
          },
          {
            label: 'Developers',
            type: 'docSidebar',
            sidebarId: 'devSidebar',
            position: 'left',
          },
          {
            label: 'API',
            type: 'docSidebar',
            sidebarId: 'apiSidebar',
            position: 'left',
          },
          {
            href: 'https://github.com/qubic/docs',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Documentation',
            items: [
              {
                label: 'Overview',
                to: '/overview/introduction',
              },
              {
                label: 'Learn',
                to: '/learn/overview',
              },
              {
                label: 'Computors',
                to: '/computors/prerequisites',
              },
              {
                label: 'Developers',
                to: '/developers/intro',
              },
              {
                label: 'API',
                to: '/api/rpc',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Discord',
                href: 'https://discord.gg/2vDMR8m',
              },
              {
                label: 'Twitter',
                href: 'https://twitter.com/qubic_network',
              },
              {
                label: 'Telegram',
                href: 'https://t.me/qubic_network',
              },
            ],
          },
          {
            title: 'Official Links',
            items: [
              {
                label: 'Careers',
                href: 'https://qubic.org/careers',
              },
              {
                label: 'Explorer',
                href: 'https://explorer.qubic.org/',
              },
              {
                label: 'GitHub',
                href: 'https://github.com/qubic/docs',
              },
              {
                label: 'Qubic Website',
                href: 'https://qubic.org/',
              },
              {
                label: 'Wallet',
                href: 'https://wallet.qubic.org/',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} qubic.org`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
      colorMode: {
        defaultMode: 'dark', // Set dark mode as default
        disableSwitch: false, // Allow users to switch between light and dark mode
        respectPrefersColorScheme: false, // Ignore the user's system preference
      },
      mermaid: {
        theme: {light: 'neutral', dark: 'forest'},
      },
    }),
  markdown: {
    mermaid: true,
  },
  themes: ['@docusaurus/theme-mermaid'],
};

module.exports = config;
