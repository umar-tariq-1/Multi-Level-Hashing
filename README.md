# Multi-Level-Hashing

## Algorithm Structure

The Algorithm in question has 2 main components which work together to deliver a Hashed Value.

| Component                         |
| --------------------------------- |
| [Tree Structure](#tree-structure) |
| [Hash Function](#hash-function)   |
| [Attack](#attack)                 |

## Tree Structure

The tree structure is inspired from Encoding Techniques. It builds a frequency dictionary from the input text file or string. For each key of the dictionary a Node. A Node object contains the _hash value_ (derived using the custom hash function explained in the next section) of the word as well as its other important parameters. These nodes are linked to temporary nodes as the children, i.e. the temporary node becomes the parent of the two nodes. This node is further joined by other temporary nodes. This copmplete algorithm constructs a Tree Structure with a final hash value at the root node. Each temporary node's hash value is derived from the hash value of its children. This cascading effect guarantees pseudo-randomness to some extent.

## Hash Function

## Attack

In our attack strategy, we first generated 10,000 random strings of the same length as the given string and computed their hashes to check for potential collisions with the hash of the original string. This extensive testing was designed to evaluate the collision resistance of the hash function using a diverse set of inputs. Additionally, we implemented a targeted approach by altering a single random character in the original string five times. For each modified string, we computed the new hash to determine if any collisions occurred. This dual approach allowed us to thoroughly test the robustness of the hash function against both random and systematic modifications.

<img src="https://github.com/umar-tariq-1/Multi-Level-Hashing/assets/97828137/0b80fb1c-fd73-49ec-b688-e7a8f62faa7b" alt="Attack Image..." width="50%"/>
