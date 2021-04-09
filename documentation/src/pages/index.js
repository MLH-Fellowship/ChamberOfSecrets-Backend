import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import useBaseUrl from '@docusaurus/useBaseUrl';
import styles from './styles.module.css';

const features = [
  {
    title: 'NOT Reinventing the Wheel',
    imageUrl: 'img/storage.png', 
    description: (
      <>
        Chamber of Secrets doesn't store the user's files on it's own. Neither do we use some premium storage the user will have to pay for. Rather, we use storage services that are absolutely free of cost and users already own! BUT, with added layers of security.
      </>
    ),
  },
  {
    title: 'Inspired by One-Who-Must-Not-Be-Named',
    imageUrl: 'img/voldermort.png', 
    description: (
      <>
        Remember how Lord Voldermort divides his soul into 7 Horcruxes in a bid to make himself immortal? We do the same with your files! We encrypt them, divide them into Horcruxes, then spread them over the file storage services the <code>you</code> own. No need to worry about data leaks anymore!
      </>
    ),
  },
  {
    title: 'Hybrid Encryption',
    imageUrl: 'img/encrypt.png', 
    description: (
      <>
        Chamber of Secrets uses a combination of symmetric and asymmetric encryption to secure user's file. On top of that, we split the encrypted file into 3 Horcruxes. To decrypt the original file, one needs access to ALL the 3 Horcruxes, the user's public key and the private key all at the same time!
      </>
    ),
  },
];

function Feature({imageUrl, title, description}) {
  const imgUrl = useBaseUrl(imageUrl);
  return (
    <div className={clsx('col col--4', styles.feature)}>
      {imgUrl && (
        <div className="text--center">
          <img className={styles.featureImage} src={imgUrl} alt={title} />
        </div>
      )}
      <h3>{title}</h3>
      <p>{description}</p>
    </div>
  );
}

export default function Home() {
  const context = useDocusaurusContext();
  const {siteConfig = {}} = context;
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="Digilocker redifined.">
      <header className={clsx('hero hero--primary', styles.heroBanner)}>
        <div className="container">
          <h1 className="hero__title">{siteConfig.title}</h1>
          <p className="hero__subtitle">{siteConfig.tagline}</p>
          <div className={styles.buttons}>
            <Link
              className={clsx(
                'button button--outline button--secondary button--lg',
                styles.getStarted,
              )}
              to="https://mlh-chamber-of-secrets.herokuapp.com/">
              Try it out!
            </Link>
          </div>
        </div>
      </header>
      <main>
        {features && features.length > 0 && (
          <section className={styles.features}>
            <div className="container">
              <div className="row">
                {features.map((props, idx) => (
                  <Feature key={idx} {...props} />
                ))}
              </div>
            </div>
          </section>
        )}
      </main>
    </Layout>
  );
}
