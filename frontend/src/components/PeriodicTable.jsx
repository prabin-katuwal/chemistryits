import React, { useEffect, useState } from "react";
import axios from "axios";

const groupColors = {
    1: { color: "bg-yellow-400" },
    2: { color: "bg-blue-400" },
    13: { color: "bg-indigo-400" },
    14: { color: "bg-purple-400" },
    15: { color: "bg-orange-400" },
    16: { color: "bg-blue-600" },
    17: { color: "bg-pink-600" },
    18: { color: "bg-green-400" },
};

const PeriodicTable = () => {
    const [elements, setElements] = useState([]);
    const [loading, setLoading] = useState(true);
    const [highlightedGroup, setHighlightedGroup] = useState(null);
    const [selectedElement, setSelectedElement] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get("http://127.0.0.1:8000/elements");
                console.log(response.data)
                setElements(response.data.elements);
            } catch (error) {
                console.error("Error fetching data:", error);
            } finally {
                setLoading(false);
            }
        };


        setTimeout(async () => fetchData(), 300);
    }, []);

    const fetchElementDetails = async (symbol) => {
        try {
            const response = await axios.get(`http://127.0.0.1:8000/element/${symbol}`);
            console.log(response)
            setSelectedElement(response.data);
        } catch (error) {
            console.error("Error fetching element details:", error);
        }
    };

    if (loading) return <div className="text-center">Loading...</div>;

    // Determine the maximum period and column for creating the grid
    const maxPeriod = Math.max(...elements.map((el) => el.period));
    const maxCol = Math.max(...elements.map((el) => el.col));

    // Create the table grid
    const table = Array.from({ length: maxPeriod }, () =>
        Array.from({ length: maxCol }, () => null)
    );

    // Fill the table with elements
    elements.forEach((element) => {
        table[element.period - 1][element.col - 1] = element;
    });

    // Handle button click: Highlight a group
    const handleClick = (group) => {
        if (highlightedGroup === group) {
            setHighlightedGroup(null); // Reset if clicked twice
        } else {
            setHighlightedGroup(group);
        }
    };

    return (
        <>
            <div className="flex flex-row gap-4">
                {/* Periodic Table Grid */}
                <div className="w-1/2">
                    {/* Periodic Table */}
                    <div className="flex flex-col gap-4 mb-3">
                        {table.map((row, rowIndex) => (
                            <div key={rowIndex} className="flex gap-2">
                                {row.map((element, colIndex) => (
                                    <div
                                        key={colIndex}
                                        onClick={() => element && fetchElementDetails(element.symbol)} // Fetch element details on click
                                        className={`w-16 h-16 flex items-center justify-center cursor-pointer  transform transition duration-200 hover:scale-110 hover:opacity-100 ${element
                                            ? `rounded-md text-white font-bold shadow-md ${groupColors[element.group]?.color || "bg-gray-300"
                                            } ${highlightedGroup === null || highlightedGroup === element.group
                                                ? "opacity-100"
                                                : "opacity-50"
                                            }`
                                            : ""
                                            }`}
                                    >
                                        {element && (
                                            <div className="text-center">
                                                <p className="text-lg">{element.symbol}</p>
                                                <p className="text-xs">{element.atomicNumber}</p>
                                            </div>
                                        )}
                                    </div>
                                ))}
                            </div>
                        ))}
                    </div>

                    {/* Group Buttons */}
                    <div>
                        <p className="mb-1"><strong>Groups : </strong></p>
                        <div className="flex flex-wrap justify-between">
                            {Object.entries(groupColors).map(([group, { color, label }]) => (
                                <button
                                    key={group}
                                    onClick={() => handleClick(Number(group))}
                                    className={`px-4 py-2 rounded-md text-white font-bold shadow-md ${color} ${highlightedGroup === Number(group) ? "opacity-90" : "opacity-30"
                                        }`}
                                >
                                    {group}
                                </button>
                            ))}
                        </div>
                    </div>
                </div>




                {/* Side Panel for Element Details */}
                <div className="w-1/2 p-4 rounded-md shadow-sm bg-gray-100">
                    {selectedElement ? (
                        <div>
                            <b>{selectedElement.name} ({selectedElement.symbol})</b>
                            <p className="text-justify">{selectedElement.name} is a chemical element and it has symbol {selectedElement.symbol} with the atomic number <u>{selectedElement.atomicNumber}</u> and an atomic mass of <u>{selectedElement.atomicMass}</u>.
                                It belongs to group <u>{selectedElement.group}</u> and period <u>{selectedElement.period}</u> of the periodic table.</p>
                            <br />

                            <table className="table-auto w-100">
                                <tbody>
                                    <tr className="table-row">
                                        <td><strong>Name</strong></td>
                                        <td>: {selectedElement.name}</td>
                                    </tr>
                                    <tr>
                                        <td><strong>Symbol</strong></td>
                                        <td>: {selectedElement.symbol}</td>
                                    </tr>
                                    <tr>
                                        <td><strong>Atomic Number</strong></td>
                                        <td>: {selectedElement.atomicNumber}</td>
                                    </tr>
                                    <tr>
                                        <td><strong>Atomic Mass</strong></td>
                                        <td>: {selectedElement.atomicMass} u</td>
                                    </tr>
                                    <tr>
                                        <td><strong>Group</strong></td>
                                        <td>: {selectedElement.group}</td>
                                    </tr>
                                    <tr>
                                        <td><strong>Period</strong></td>
                                        <td>: {selectedElement.period}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    ) : (
                        <p className="text-center items-center">Select an element to see details</p>
                    )}
                </div>
            </div>
            <br />
            <hr />
        </>
    );
};

export default PeriodicTable;
