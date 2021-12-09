import "./ResultItem.css";

import React from "react";
import Image from "../Image/Image";

const IMAGE_SCALE = 1;

class ResultItem extends React.Component {
    render() {
        return (
            <div className="result_item">
                <Image width={110*IMAGE_SCALE} height={170*IMAGE_SCALE} src={this.props.data.poster_url} />
                <div className="description">
                    <span className="movie_name">{this.props.data.movie_name}</span>
                    <span className="movie_match">{Math.round(this.props.data.match * 100)}% Match</span>
                </div>
            </div>
        );
    }
}

export default ResultItem;
