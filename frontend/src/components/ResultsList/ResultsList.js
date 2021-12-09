import "./ResultsList.css";

import React from "react";
import ResultItem from "../ResultItem/ResultItem";

class Results extends React.Component {
    render() {
        return (
            <div className="result_list">
                {this.props.results?.map((result, index) => (
                    <div style={{ animationDelay: `${index/3}s` }} key={index} className="result_list_item_wrapper">
                        <div className="result_list_number">{index + 1}</div>
                        <div className="result_item_content_wrapper">
                            <ResultItem key={index} data={result} />
                        </div>
                    </div>
                ))}
            </div>
        );
    }
}

export default Results;
