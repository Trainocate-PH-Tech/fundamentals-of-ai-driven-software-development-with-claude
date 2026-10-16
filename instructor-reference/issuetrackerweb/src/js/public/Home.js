import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faArrowRight,
  faChartLine,
  faCircleCheck,
  faGaugeHigh,
  faShieldHalved
} from "@fortawesome/free-solid-svg-icons";
import { Link } from "react-router-dom";

const capabilities = [
  {
    description: "See service health, account activity, and operational priorities in one place.",
    icon: faGaugeHigh,
    title: "Clear oversight"
  },
  {
    description: "Keep administrative workflows protected with role-aware access controls.",
    icon: faShieldHalved,
    title: "Secure by default"
  },
  {
    description: "Turn reliable operational data into faster, more confident decisions.",
    icon: faChartLine,
    title: "Actionable insight"
  }
];

const Home = () => {
  return (
    <>
      <section className="public-hero">
        <div className="container">
          <div className="row align-items-center g-5">
            <div className="col-12 col-lg-7">
              <div className="public-eyebrow">
                <span className="public-eyebrow-dot" />
                Operations, brought into focus
              </div>
              <h1 className="public-hero-title">
                Run your business with clarity and control.
              </h1>
              <p className="public-hero-copy">
                CloudBand gives operations teams a dependable workspace for managing
                users, monitoring services, and keeping everyday administration moving.
              </p>
              <div className="d-flex flex-wrap gap-3">
                <Link className="btn btn-primary btn-lg public-primary-action" to="/login">
                  <span>Open admin panel</span>
                  <FontAwesomeIcon icon={faArrowRight} />
                </Link>
                <Link className="btn btn-outline-dark btn-lg" to="/about">
                  Learn about CloudBand
                </Link>
              </div>
            </div>

            <div className="col-12 col-lg-5">
              <div className="public-overview-card">
                <div className="public-overview-header">
                  <div>
                    <span className="public-overview-label">Platform overview</span>
                    <h2 className="h5 mb-0">Everything is operating normally</h2>
                  </div>
                  <span className="public-status-indicator">
                    <FontAwesomeIcon icon={faCircleCheck} />
                  </span>
                </div>

                <div className="public-overview-metrics">
                  <div className="public-overview-metric">
                    <span>Availability</span>
                    <strong>99.99%</strong>
                  </div>
                  <div className="public-overview-metric">
                    <span>Active services</span>
                    <strong>24</strong>
                  </div>
                </div>

                <div className="public-service-list">
                  {["Identity services", "Account management", "System API"].map((service) => {
                    return (
                      <div className="public-service-row" key={service}>
                        <span>{service}</span>
                        <span className="public-service-status">Operational</span>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="public-section">
        <div className="container">
          <div className="public-section-heading">
            <span className="public-section-kicker">Built for daily operations</span>
            <h2>A practical foundation for teams that need to move.</h2>
            <p>
              Purposeful tools, a focused interface, and the information your team needs
              to act without unnecessary complexity.
            </p>
          </div>

          <div className="row g-4">
            {capabilities.map((capability) => {
              return (
                <div className="col-12 col-md-4" key={capability.title}>
                  <article className="public-feature-card h-100">
                    <span className="public-feature-icon">
                      <FontAwesomeIcon icon={capability.icon} />
                    </span>
                    <h3>{capability.title}</h3>
                    <p>{capability.description}</p>
                  </article>
                </div>
              );
            })}
          </div>
        </div>
      </section>
    </>
  );
};

export default Home;
