const fs = require('fs');
const replacement = `  <g id="robot" stroke="#092b5c" stroke-width="3.4" stroke-linejoin="round" stroke-linecap="round">
    <!-- Right Wheels (back layer) -->
    <ellipse cx="6" cy="18" rx="8" ry="11" fill="#59baff" />
    <ellipse cx="22" cy="12" rx="8" ry="11" fill="#59baff" />

    <!-- Body Top (parallelogram) -->
    <polygon points="-24,-5 5,-14 20,-11 -9,-2" fill="#2d8fcf" />
    <!-- Body Front (vertical parallelogram) -->
    <polygon points="-9,-2 20,-11 20,4 -9,13" fill="url(#robot-fill)" />
    <!-- Body Left (side parallelogram) -->
    <polygon points="-24,-5 -9,-2 -9,13 -24,4" fill="#4ab2f7" />

    <!-- Head Top (parallelogram) -->
    <polygon points="-16,-20 -2,-25 7,-23 -7,-18" fill="#2d8fcf" />
    <!-- Head Left (side parallelogram) -->
    <polygon points="-16,-20 -7,-18 -7,-9 -16,-11" fill="#4ab2f7" />
    <!-- Head Front (vertical parallelogram) -->
    <polygon points="-7,-18 7,-23 7,-14 -7,-9" fill="#75c5ff" />
    
    <!-- Eyes -->
    <circle cx="-1" cy="-14.5" r="2" fill="#eefaff" stroke-width="2" />
    <circle cx="4" cy="-16" r="2" fill="#eefaff" stroke-width="2" />

    <!-- Left Wheels (front layer) -->
    <ellipse cx="-20" cy="14" rx="8" ry="11" fill="#59baff" />
    <ellipse cx="-4" cy="22" rx="8" ry="11" fill="#59baff" />
  </g>`;

['assets/svg-components/robot.svg', 'assets/zenoh-pub-sub.svg', 'assets/zenoh-query.svg'].forEach(file => {
  let content = fs.readFileSync(file, 'utf8');
  content = content.replace(/<g id="robot"[\s\S]*?<\/g>/, replacement);
  fs.writeFileSync(file, content);
});
