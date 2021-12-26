import "./ResultItem.css";

import React from "react";
import Image from "../Image/Image";

const IMAGE_SCALE = 1;

class ResultItem extends React.Component {
    render() {
        console.log(this.props.data);
        return (
            <div className="result_item">
                <Image
                    width={200 * IMAGE_SCALE}
                    height={112 * IMAGE_SCALE}
                    contain={!this.props.data.metadata.backdrop_path}
                    src={this.props.data.metadata.backdrop_path ?? this.props.data.metadata.poster_path}
                />
                <div className="description">
                    <span className="movie_name">{this.props.data.movie_name}</span>
                    <span className="movie_match">{Math.round(this.props.data.match * 100)}% Match</span>
                </div>
            </div>
        );
    }
}

export default ResultItem;
