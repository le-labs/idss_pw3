import "./App.css";
import SearchBar from "./Searchbar";
import Results from "./Results";

import React, {useState} from "react";

class App extends React.Component {

    state = {
        results:[],
    }

    async loadRecommendations(movie_name) {
        const result = await (await fetch("http://127.0.0.1:5000/recommend?title=" + encodeURIComponent(movie_name))).json();
        
        this.setState({
            results: result.data,
        })
    }

    render() {
        return (
            <div className="App">
                <div class="title_container">
                    <h1>Flix Recommender</h1>
                </div>
                <div class="searchbar_container">
                    <SearchBar searchCallback={(m) => this.loadRecommendations(m)} />
                </div>
                <div class="results_container">
                    <Results results={this.state.results} />
                </div>
            </div>
        );
    }
}

export default App;
