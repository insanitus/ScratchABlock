// Graph props:
//  name: None
//  trailing_jumps: True

// Predecessors: []
05.if:
if ($a1 == 5) {
  $a4 = 2
  $a2 = 5
} else {
  $a2 = 1
}
Exits: [(None, '20')]

// Predecessors: ['05.if']
20:
$a3 = 3
Exits: []
