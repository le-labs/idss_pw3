import "./MovieDetailsModal.css";
import React from "react";
import ReactModal from "react-modal";

import Image from "../Image/Image";

class MovieDetailsModal extends React.Component {
    render() {
        const year = this.props.data?.release_date?.split("-")?.[0];
        const rating = this.props.data?.vote_average;
        return (
            <ReactModal
                isOpen={this.props.isOpen}
                preventScroll={true}
                className="modal_body"
                overlayClassName="modal_overlay"
                ariaHideApp={false}
            >
                <i className="gg-close close_button" onClick={() => this.props.onClose()}></i>
                <div className="movie_details_container">
                    <Image src={this.props.data.poster_path} height={300} width={300 / 1.5} />
                    <div className="movie_details_text_container">
                        <div className="movie_title">
                            <span className="movie_name">{this.props.data.netflix_title}</span>
                            {year && <span className="movie_year">{year}</span>}
                            {rating && <span className="movie_rating">{rating}/10</span>}
                            <span className="movie_match">{Math.round(this.props.match * 100)}% Match</span>
                        </div>
                        {this.props.data.overview && <span>{this.props.data.overview}</span>}

                        <div className="watch_button_container">
                            <a
                                className="watch_button"
                                href={`https://www.netflix.com/search?q=${encodeURIComponent(
                                    this.props.data.netflix_title
                                )}`}
                                target="_blank"
                            >
                                <i
                                    className="gg-play-button"
                                    style={{ display: "inline-block", verticalAlign: "bottom", marginRight: "10px" }}
                                ></i>
                                <span>Play</span>
                            </a>
                        </div>

                        {this.props.data.genres && (
                            <div className="genre_container">
                                {this.props.data.genres.map((g, i) => (
                                    <span className="genre_badge" key={i}>
                                        {g}
                                    </span>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            </ReactModal>
        );
    }
}

export default MovieDetailsModal;
