const SearchBarStyle = {
    option: (provided, state) => ({
        ...provided,
        border: "1px solid white",
        color: state.isSelected ? "#e50914" : "white",
        backgroundColor: "#222",
        fontSize: "20px",
        padding: 10,
        "&:hover": {
            backgroundColor: "#333",
        },
    }),
    control: () => ({
        width: "100%",
        color: "white",
        borderBottom: "5px solid white",
    }),
    valueContainer: provided => ({
        ...provided,
        padding: "0 0 1px 0",
    }),
    input: provided => ({
        ...provided,
        fontSize: "50px",
        color: "#e50914",
    }),
    singleValue: provided => ({
        ...provided,
        fontSize: "50px",
        color: "#e50914",
    }),
    placeholder: provided => ({
        ...provided,
        fontSize: "50px",
        color: "#585858",
    }),
    menu: provided => ({
        ...provided,
        borderRadius: 0,
    }),
    menuList: () => ({
        padding: 0,
        backgroundColor: "#141414",
    }),
};

export default SearchBarStyle;
