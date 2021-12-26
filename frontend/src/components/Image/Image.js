import "./Image.css";
import React from "react";

class Image extends React.Component {
    render() {
        if (this.props.src) {
            return (
                <div style={{ width: this.props.width, height: this.props.height }} className="image_wrapper shimmer">
                    {this.props.contain && <img className="background_image" src={this.props.src} alt="" />}
                    <img style={{ objectFit: this.props.contain ? "contain" : "cover" }} src={this.props.src} alt="" />
                </div>
            );
        } else {
            return (
                <div
                    style={{ width: this.props.width, height: this.props.height }}
                    className="image_wrapper image_placeholder"
                ></div>
            );
        }
    }
}

export default Image;
