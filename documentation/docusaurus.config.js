/** @type {import('@docusaurus/types').DocusaurusConfig} */
module.exports = {
  title: 'Chamber of Secrets',
  tagline: 'Digi-Locker redefined, inspired by Lord Voldermort.',
  url: 'https://chamber-of-secrets.netlify.app',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/ChamberOfSecrets.png',
  organizationName: 'MLH-Fellowship', // Usually your GitHub org/user name.
  projectName: 'ChamberOfSecrets', // Usually your repo name.
  themeConfig: {
    navbar: {
      title: 'Chamber of Secrets', 
      logo: {
        alt: 'Chamber of Secrets',
        src: 'img/ChamberOfSecrets.png', 
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
          href: 'https://github.com/MLH-Fellowship/Chamber-of-Secrets', 
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
              href: 'https://github.com/MLH-Fellowship/Chamber-of-Secrets',
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
