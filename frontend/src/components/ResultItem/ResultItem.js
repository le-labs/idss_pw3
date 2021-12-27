import "./ResultItem.css";

import React from "react";
import Image from "../Image/Image";
import MovieDetailsModal from "../MovieDetailsModal/MovieDetailsModal";

const IMAGE_SCALE = 1;

class ResultItem extends React.Component {
    state = {
        showDetailsModal: false,
    };

    openModal() {
        this.setState({ showDetailsModal: true });
    }

    closeModal() {
        this.setState({ showDetailsModal: false });
    }

    render() {
        return (
            <div className="result_item" onClick={() => !this.state.showDetailsModal ? this.openModal(): null}>
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
                <MovieDetailsModal
                    isOpen={this.state.showDetailsModal}
                    data={this.props.data.metadata}
                    match={this.props.data.match}
                    onClose={this.closeModal.bind(this)}
                />
            </div>
        );
    }
}

export default ResultItem;
