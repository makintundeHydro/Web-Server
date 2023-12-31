const data = {
    location: 'Branmd',
    busNumbers: ['2', '3'],
    machine_seq_table: [
      ['2', '1', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3'],
      ['3', '2', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3'],
    ],
    two_winding_table: [
      [
        '3333',
        '2',
        '1',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
        '2',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
      ],
      [
        '3333',
        '3',
        '2',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
        '2',
        '3',
        '3',
        '3',
        '3',
        '3',
        '3',
      ],
    ],
    Model: {
      Generator: {
        GENSAL: {
          bus: [{ bus: '2', id: '1' }],
          con: [
            {
              col1: 'j',
              col2: 'D-Axis Opened Circuit Transient Time Constant',
              col3: "T'do (> 0)",
              col4: '3',
            },
            {
              col1: 'j+1',
              col2: 'D-Axis Opened Circuit Sub-transient Time Constant',
              col3: "T''do (> 0)",
              col4: '3',
            },
            {
              col1: 'j+2',
              col2: 'Q-Axis Opened Circuit Transient Time Constant',
              col3: "T'qo (> 0)",
              col4: '3',
            },
            {
              col1: 'j+3',
              col2: 'Q-Axis Opened Circuit Sub-transient Time Constant',
              col3: "T''qo (> 0)",
              col4: '3',
            },
            { col1: 'j+4', col2: 'Inertia', col3: 'H', col4: '3' },
            { col1: 'j+5', col2: 'Speed Damping', col3: 'D', col4: '3' },
            {
              col1: 'j+6',
              col2: 'D-Axis Synchronous Reactance',
              col3: 'Xd',
              col4: '3',
            },
            {
              col1: 'j+7',
              col2: 'Q-Axis Synchronous Reactance',
              col3: 'Xq',
              col4: '3',
            },
            {
              col1: 'j+8',
              col2: 'D-Axis Transient Reactance',
              col3: "X'd",
              col4: '3',
            },
            {
              col1: 'j+9',
              col2: 'Q-Axis Transient Reactance',
              col3: "X'q",
              col4: '3',
            },
            {
              col1: 'j+10',
              col2: 'D/Q-Axis Sub-transient Reactance',
              col3: "X''d = X''q",
              col4: '3',
            },
            { col1: 'j+11', col2: 'Leakage Reactance', col3: 'Xl', col4: '3' },
            {
              col1: 'j+12',
              col2: 'Open Circuit Saturation Factor',
              col3: 'S(1.0)',
              col4: '3',
            },
            {
              col1: 'j+13',
              col2: 'Open Circuit Saturation Factor',
              col3: 'S(1.2)',
              col4: '3',
            },
          ],
          icon: [],
        },
      },
    },
  };

  