import * as React from "react";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Button from "@mui/material/Button";
import logo from "../logo.png";

const styles = {
  buttonColor: {
    color: "#26B0B2",
    marginLeft: "auto",
    marginRight: "15px",
  },
  navText:{
      marginLeft: "15px",
      color:'#26B0B2'
  }
};

export const NavBar = () => {
  return (
    <Box>
      <AppBar
        position="static"
        style={{
          background: "#FFFFFF",
          borderBottom: "1pt solid #26B0B2",
          boxShadow: "none",
        }}
      >
        <Toolbar>
        <img src={logo} alt="Company logo" height={28} width={50} />
        <span style={styles.navText}>
            LOCATION LOOKUP RESOURCE
        </span>
          <Button
            style={styles.buttonColor}
            target="_blank"
            href="https://www.carnallfarrar.com/"
          >
            About CF
          </Button>
        </Toolbar>
      </AppBar>
    </Box>
  );
};
