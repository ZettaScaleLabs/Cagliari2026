const fs = require('fs');
const replacement = `  <g id="robot" stroke="#092b5c" stroke-width="3.4" stroke-linejoin="round" stroke-linecap="round">
    <!-- Right Wheels -->
    <ellipse cx="7" cy="11" rx="8" ry="11" fill="#59baff" />
    <ellipse cx="23" cy="19" rx="8" ry="11" fill="#59baff" />

    <!-- Body Top -->
    <polygon points="-9,-5 21,-1 5,-7 -25,-11" fill="#2d8fcf" />
    <!-- Body Left -->
    <polygon points="-25,-11 -9,-5 -5,5 -5,15 -25,3" fill="#4ab2f7" />
    <!-- Body Front Slanted -->
    <polygon points="-9,-5 21,-1 25,9 -5,5" fill="#59baff" />
    <!-- Body Front Vertical -->
    <polygon points="-5,5 25,9 25,19 -5,15" fill="url(#robot-fill)" />

    <!-- Head Top -->
    <polygon points="-11,-18 5,-16 -5,-20 -21,-22" fill="#2d8fcf" />
    <!-- Head Left -->
    <polygon points="-21,-22 -11,-18 -11,-6 -21,-10" fill="#4ab2f7" />
    <!-- Head Front -->
    <polygon points="-11,-18 5,-16 5,-4 -11,-6" fill="#75c5ff" />
    
    <!-- Eyes -->
    <circle cx="-5" cy="-12" r="2.5" fill="#eefaff" stroke-width="2.5" />
    <circle cx="1" cy="-11" r="2.5" fill="#eefaff" stroke-width="2.5" />

    <!-- Left Wheels -->
    <ellipse cx="-21" cy="7" rx="8" ry="11" fill="#59baff" />
    <ellipse cx="-7" cy="17" rx="8" ry="11" fill="#59baff" />
  </g>`;

['assets/svg-components/robot.svg', 'assets/zenoh-pub-sub.svg', 'assets/zenoh-query.svg'].forEach(file => {
  let content = fs.readFileSync(file, 'utf8');
  content = content.replace(/<g id="robot"[\s\S]*?<\/g>/, replacement);
  fs.writeFileSync(file, content);
});
