import "./Searchbar.css";
import { Typeahead } from "react-typeahead";

import TitlesMap from "./data/titles.json";
import React from "react";

const titles = Object.values(TitlesMap);

class SearchBar extends React.Component {
    render() {
        return (
            <Typeahead
                onOptionSelected={this.props.searchCallback}
                options={titles}
                maxVisible={5}
                className="searchbar"
                customClasses={{
                    input: "searchbar-text-input",
                    results: "searchbar-list__container",
                    listItem: "searchbar-list__item",
                }}
            />
        );
    }
}

export default SearchBar;
