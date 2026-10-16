import React from "react";
import { Outlet } from "react-router-dom";
import Content from "./Content";
import Header from "./Header";

const Layout = () => {
  return (
    <div className="public-layout">
      <Header />
      <Content>
        <Outlet />
      </Content>
    </div>
  );
};

export default Layout;
