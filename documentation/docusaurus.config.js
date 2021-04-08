/** @type {import('@docusaurus/types').DocusaurusConfig} */
module.exports = {
  title: 'Chamber of Secrets',
  tagline: 'Digi-locker redifined, inspired by Lord Voldermort.',
  url: 'https://github.com/MLH-Fellowship.github.io',
  baseUrl: '/ChamberOfSecrets-Backend/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: 'MLH-Fellowship', // Usually your GitHub org/user name.
  projectName: 'ChamberOfSecrets', // Usually your repo name.
  themeConfig: {
    navbar: {
      title: 'Chamber of Secrets', 
      logo: {
        alt: 'My Site Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          to: 'docs/chamber-of-secrets',
          activeBasePath: 'docs',
          label: 'Docs',
          position: 'left',
        },
        {
          href: 'https://github.com/MLH-Fellowship/ChamberOfSecrets-Backend', 
          label: 'GitHub-Server',
          position: 'right',
        },
        {
          href: 'https://github.com/MLH-Fellowship/DigiCrux', 
          label: 'GitHub-Client',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Getting Started',
              to: 'docs/chamber-of-secrets',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'GitHub-Server',
              href: 'https://github.com/MLH-Fellowship/ChamberOfSecrets-Backend',
            },
            {
              label: 'GitHub-Client',
              href: 'https://github.com/MLH-Fellowship/DigiCrux',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Chamber of Secrets, Inc. Built with Docusaurus.`,
    },
  },
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          // Please change this to your repo.
          editUrl:
            'https://github.com/MLH-Fellowship/ChamberOfSecrets-Backend/documentation/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],
};
