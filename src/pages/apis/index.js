import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';

const apis = [
  {
    title: 'Query API',
    description: 'Access historical blockchain data, transactions, and archived information.',
    link: '/apis/query#description/introduction',
  },
  {
    title: 'Live API',
    description: 'Real-time interaction with the Qubic network. Submit transactions, check balances, and monitor network status.',
    link: '/apis/live#description/introduction',
    badge: 'REST',
  },
];

function ApiCard({ title, description, link, badge }) {
  return (
    <Link to={link} className="api-card">
      <div className="api-card-content">
        <div className="api-card-header">
          <h3>{title}</h3>
          {badge && <span className="api-badge">{badge}</span>}
        </div>
        <p>{description}</p>
      </div>
    </Link>
  );
}

export default function ApisPage() {
  return (
    <Layout title="API Center" description="Qubic API Documentation">
      <div className="apis-container">
        <div className="apis-hero">
          <h1>Qubic API Center</h1>
          <p>Explore our APIs to build powerful integrations with the Qubic network.</p>
        </div>
        <div className="apis-grid">
          {apis.map((api, idx) => (
            <ApiCard key={idx} {...api} />
          ))}
        </div>
      </div>
    </Layout>
  );
}
