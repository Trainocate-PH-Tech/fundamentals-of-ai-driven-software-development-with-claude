import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faArrowRight,
  faCompass,
  faHandshake,
  faLightbulb
} from "@fortawesome/free-solid-svg-icons";
import { Link } from "react-router-dom";

const principles = [
  {
    description: "We reduce noise so teams can focus on the work that moves the business forward.",
    icon: faCompass,
    title: "Clarity over complexity"
  },
  {
    description: "We build dependable foundations and make security part of every workflow.",
    icon: faHandshake,
    title: "Trust through consistency"
  },
  {
    description: "We improve with purpose, guided by real operational needs and measurable outcomes.",
    icon: faLightbulb,
    title: "Progress with intent"
  }
];

const About = () => {
  return (
    <>
      <section className="public-about-hero">
        <div className="container">
          <div className="row g-5 align-items-end">
            <div className="col-12 col-lg-8">
              <span className="public-section-kicker">About CloudBand</span>
              <h1>Better operations begin with a clearer view.</h1>
            </div>
            <div className="col-12 col-lg-4">
              <p className="public-about-lead">
                We create focused administrative tools that help growing teams work
                securely, respond quickly, and operate with confidence.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="public-section public-about-story">
        <div className="container">
          <div className="row g-5 align-items-center">
            <div className="col-12 col-lg-5">
              <div className="public-story-panel">
                <span className="public-story-number">01</span>
                <p>One reliable workspace for the people responsible for keeping systems and services on track.</p>
              </div>
            </div>
            <div className="col-12 col-lg-7">
              <span className="public-section-kicker">Our purpose</span>
              <h2 className="public-story-title">Technology should make responsibility feel manageable.</h2>
              <p className="public-story-copy">
                Administrative work is often spread across disconnected tools and hidden
                behind unnecessary friction. CloudBand brings the essential workflows
                together in a straightforward environment designed for real operating teams.
              </p>
              <p className="public-story-copy mb-0">
                The result is a calmer, more accountable way to manage access, understand
                service health, and make informed decisions as the organization grows.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="public-section public-principles-section">
        <div className="container">
          <div className="public-section-heading">
            <span className="public-section-kicker">How we work</span>
            <h2>Principles that shape the platform.</h2>
          </div>

          <div className="row g-4">
            {principles.map((principle) => {
              return (
                <div className="col-12 col-md-4" key={principle.title}>
                  <article className="public-principle-card h-100">
                    <FontAwesomeIcon icon={principle.icon} />
                    <h3>{principle.title}</h3>
                    <p>{principle.description}</p>
                  </article>
                </div>
              );
            })}
          </div>

          <div className="public-about-cta">
            <div>
              <span className="public-section-kicker">Ready when you are</span>
              <h2>Put a clearer operating system to work.</h2>
            </div>
            <Link className="btn btn-light btn-lg" to="/login">
              <span>Sign in to CloudBand</span>
              <FontAwesomeIcon icon={faArrowRight} />
            </Link>
          </div>
        </div>
      </section>
    </>
  );
};

export default About;
