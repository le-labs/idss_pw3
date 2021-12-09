import React, { useMemo, useState } from "react";
import Select from "react-select";
import escapeRegExp from "lodash.escaperegexp";

import SearchBarStyle from "./SearchBarStyle";

function SearchBar(props) {
    const [inputValue, setInputValue] = useState("");

    const filteredOptions = useMemo(() => {
        if (!inputValue) {
            return props.options;
        }
        const re = new RegExp(escapeRegExp(inputValue), "i");
        return props.options.filter(op => re.test(op.label));
    }, [inputValue, props.options]);

    const slicedOptions = useMemo(
        () => filteredOptions.slice(0, props.maxResults ?? 8),
        [filteredOptions, props.maxResults]
    );

    return (
        <Select
            options={slicedOptions}
            onInputChange={value => setInputValue(value)}
            components={{ DropdownIndicator: null }}
            filterOption={() => true} // disable native filter
            placeholder="..."
            styles={SearchBarStyle}
            onChange={props.searchCallback}
        />
    );
}

export default SearchBar;
