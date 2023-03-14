import React, { Component } from 'react';
import { gantt } from 'dhtmlx-gantt'; // убрать потом
import 'dhtmlx-gantt';
import 'dhtmlx-gantt/codebase/dhtmlxgantt.css';

class Gantt extends Component {
    componentDidMount() {

        gantt.config.date_format = "%Y-%m-%d %H:%i";
        const { tasks } = this.props;
        gantt.init(this.ganttContainer);
        gantt.parse(tasks);

        // fetch('http://localhost:8000/api/v1/gant')
        //     .then(response => response.json())
        //     .then(data => {
        //         gantt.config.xml_date = '%Y-%m-%d %H:%i';
        //         gantt.init(this.ganttContainer);
        //         gantt.parse({ data: data });
        //     });
    }

    render() {
        return (
            <div
                ref={(input) => { this.ganttContainer = input }}
                style={{ width: 'q00%', height: '500px' }}
            ></div>
        );
    }
}

export default Gantt;