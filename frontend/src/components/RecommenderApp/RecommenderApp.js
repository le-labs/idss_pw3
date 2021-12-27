import "./RecommenderApp.css";

import React from "react";

import SearchBar from "../SearchBar/SearchBar";
import ResultsList from "../ResultsList/ResultsList";
import LoadingSpinner from "../LoadingSpinner/LoadingSpinner";

import titles_data from "../../data/titles.json";
const options = Object.values(titles_data).map(v => ({ value: v, label: v }));

class RecommenderApp extends React.Component {
    state = {
        results: [],
        loading: false,
        error: null,
    };

    loadRecommendations(movie_name) {
        this.setState({ loading: true, results: [], error: null });

        fetch("http://127.0.0.1:5000/recommend?title=" + encodeURIComponent(movie_name))
            .then(r => r.json())
            .then(data => {
                if (data.message) {
                    throw data.message;
                }
                const results = data.data.map(el => ({
                    movie_name: el.Name,
                    match: el.PearsonR,
                    metadata: el.metadata,
                }));
                this.setState({
                    results: results,
                    loading: false,
                    error: null,
                });
            })
            .catch(reason => {
                console.log("Failed to load recommendations:", reason);
                this.setState({ loading: false, error: reason.toString() });
            });
    }

    render() {
        return (
            <div className="app_container">
                <div className="app_container_inner">
                    <div className="title_container">
                        What <span className="netflix_red">movie</span> should i watch when i like &nbsp;
                        <div className="searchbar_container">
                            <SearchBar
                                searchCallback={m => this.loadRecommendations(m.label)}
                                maxResults={8}
                                options={options}
                            />
                        </div>
                        &nbsp;?
                    </div>
                    {this.state.loading && (
                        <div className="loading_container">
                            <LoadingSpinner />
                        </div>
                    )}
                    {this.state.error && <div className="error_container">{this.state.error}</div>}
                    {this.state.results && (
                        <div className="results_container">
                            <ResultsList results={this.state.results} />
                        </div>
                    )}
                </div>
            </div>
        );
    }
}

export default RecommenderApp;
