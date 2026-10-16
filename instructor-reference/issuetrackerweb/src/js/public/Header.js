import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faArrowRight,
  faLayerGroup
} from "@fortawesome/free-solid-svg-icons";
import { Link, NavLink } from "react-router-dom";

const navigationItems = [
  {
    label: "Home",
    path: "/"
  },
  {
    label: "About",
    path: "/about"
  }
];

const Header = () => {
  return (
    <header className="public-header">
      <div className="container public-header-inner">
        <Link className="public-brand" to="/" aria-label="CloudBand home">
          <span className="public-brand-mark">
            <FontAwesomeIcon icon={faLayerGroup} />
          </span>
          <span>CloudBand</span>
        </Link>

        <nav className="public-navigation" aria-label="Primary navigation">
          {navigationItems.map((item) => {
            return (
              <NavLink
                className={({ isActive }) => {
                  return `public-navigation-link ${isActive ? "active" : ""}`;
                }}
                end={item.path === "/"}
                key={item.path}
                to={item.path}
              >
                {item.label}
              </NavLink>
            );
          })}
        </nav>

        <Link className="btn btn-dark public-header-action" to="/login">
          <span>Sign in</span>
          <FontAwesomeIcon icon={faArrowRight} />
        </Link>
      </div>
    </header>
  );
};

export default Header;
