import React from "react";
import "./Results.css";


class Results extends React.Component {
    render() {
        return (
            <div className="results">
                <ul class="result_list">
                    {this.props.results?.map((r,index) => {
                        return (
                            <li class="result_item" key={index}>
                                <img src={r.poster_url} />
                                <div class="description">
                                    <span class="movie_name">{r.Name}</span>
                                    <span class="movie_match">{Math.round(r.PearsonR * 100)}% Match</span>
                                </div>
                            </li>
                        )
                    })}
                </ul>
            </div>
        );
    }
}

export default Results;
