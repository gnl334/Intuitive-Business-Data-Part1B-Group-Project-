import { useState } from "react";
import "./PolicyCreator.css";

function PolicyCreator() {
    const [blocksPanelExpanded, setBlocksPanelExpanded] = useState(false);

    return (
        <div className="policy-creator">
            {/* Header with Save Button */}
            <header className="policy-header">
                <button className="save-btn">Save</button>
            </header>

            {/* Main Content Area */}
            <div className="policy-container">
                {/* Left Sidebar - Policies/Templates */}
                <aside className="policy-sidebar">
                    <div className="sidebar-header">
                        <h3>Templates</h3>
                    </div>
                    <div className="sidebar-search">
                        <input type="text" placeholder="🔍 Search" />
                    </div>
                    <div className="template-list">
                        <div className="template-item">Template 1</div>
                        <div className="template-item">Template 2</div>
                        <div className="template-item">Template 5</div>
                    </div>
                </aside>

                {/* Center Canvas Area */}
                <main className="flowchart-canvas">
                    <div className="canvas-placeholder">
                        <p>Flowchart Editor Canvas</p>
                    </div>
                </main>
            </div>

            {/* Bottom Panel - Flowchart Blocks Library */}
            <div
                className={`blocks-panel ${blocksPanelExpanded ? "expanded" : "collapsed"}`}
            >
                <div className="blocks-header">
                    <button
                        className="expand-toggle"
                        onClick={() =>
                            setBlocksPanelExpanded(!blocksPanelExpanded)
                        }
                    >
                        {blocksPanelExpanded ? "▼" : "▲"} Blocks Library
                    </button>
                </div>

                {blocksPanelExpanded && (
                    <div className="blocks-content">
                        <div className="block-category">
                            <h4>Inputs</h4>
                            <div className="block-items">
                                <div className="block-item">Input Block</div>
                            </div>
                        </div>

                        <div className="block-category">
                            <h4>Components</h4>
                            <div className="block-items">
                                <div className="block-item">Process Block</div>
                                <div className="block-item">Decision Block</div>
                            </div>
                        </div>

                        <div className="block-category">
                            <h4>Outputs</h4>
                            <div className="block-items">
                                <div className="block-item">Output Block</div>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default PolicyCreator;
