import "./LoadingSpinner.css";
import React from "react";

class LoadingSpinner extends React.Component {
    render() {
        return <div className="lds-dual-ring"></div>;
    }
}

export default LoadingSpinner;
