import {Categories, Issues, IssueForm, IssueDetails} from './tracker/Tracker';
import React, { useEffect, useState } from "react";
import Login from "./Login";
import { AUTH_STATE_CHANGE_EVENT, isLoggedIn } from "./services/AuthService";
import Sidebar from "./Sidebar";
import TopNavigation from "./TopNavigation";
import {
  Navigate,
  Routes,
  Route
} from "react-router-dom";

import Dashboard from "./Dashboard";
import Settings from "./Settings";
import UsersIndex from "./users/Index";
import UsersShow from "./users/Show";
import UsersForm from "./users/Form";
import About from "./public/About";
import Home from "./public/Home";
import PublicLayout from "./public/Layout";

const PublicApp = () => {
  return (
    <Routes>
      <Route element={<PublicLayout />}>
        <Route
          path="/"
          element={<Home />}
        />
        <Route
          path="/about"
          element={<About />}
        />
      </Route>
      <Route
        path="/login"
        element={<Login />}
      />
      <Route
        path="*"
        element={<Navigate to="/" replace />}
      />
    </Routes>
  );
};

const AuthenticatedApp = () => {
  return (
    <div className="app-container">
      <Sidebar />
      <div className="app-main-section">
        <TopNavigation />
        <main className="app-page-shell container-fluid px-3">
          <Routes>
            <Route path="/categories" element={<Categories />} />
            <Route path="/issues" element={<Issues />} />
            <Route path="/issues/new" element={<IssueForm />} />
            <Route path="/issues/:id/edit" element={<IssueForm />} />
            <Route path="/issues/:id" element={<IssueDetails />} />
            <Route
              path="/"
              element={<Navigate to="/dashboard" replace />}
            />
            <Route
              path="/login"
              element={<Navigate to="/dashboard" replace />}
            />
            <Route
              path="/dashboard"
              element={<Dashboard />}
            />
            <Route
              path="/settings"
              element={<Settings />}
            />
            <Route
              path="/users"
              element={<UsersIndex />}
            />
            <Route
              path="/users/new"
              element={<UsersForm />}
            />
            <Route
              path="/users/:id"
              element={<UsersShow />}
            />
            <Route
              path="/users/:id/edit"
              element={<UsersForm />}
            />
            <Route
              path="*"
              element={<Navigate to="/dashboard" replace />}
            />
          </Routes>
        </main>
      </div>
    </div>
  );
};

const App = () => {
  const [authenticated, setAuthenticated] = useState(isLoggedIn());

  useEffect(() => {
    const syncAuthenticationState = () => {
      setAuthenticated(isLoggedIn());
    };

    window.addEventListener(AUTH_STATE_CHANGE_EVENT, syncAuthenticationState);
    window.addEventListener("storage", syncAuthenticationState);
    window.addEventListener("hashchange", syncAuthenticationState);

    return () => {
      window.removeEventListener(AUTH_STATE_CHANGE_EVENT, syncAuthenticationState);
      window.removeEventListener("storage", syncAuthenticationState);
      window.removeEventListener("hashchange", syncAuthenticationState);
    };
  }, []);

  if (authenticated) {
    return <AuthenticatedApp />;
  }

  return <PublicApp />;
};

export default App;
