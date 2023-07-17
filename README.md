# Evolution Sim
This is an evolution simulator!<br>
the debug keys are:<ul>
<li>F : Advances by one frame and pauses</li>
<li>Space : toggle pauses the simulation</li>
<li>P : prints the best 4 cells in the 4 catagories</li>
<li>G : will stop food generation, starving the cells</li>
<li>Clicking :<ul>
    <li>On an exisiting cell<ul>
        <li>Once : will print the stats and genetics of the cell</li>
        <li>Thrice+ : will attempt to remove the cell</li>
    </li></ul>
    <li>On a cell that doesnt exist will spawn a new cell</li>
</li>
</ul>
The three stats that the sim cares about are: Generation, Speed, Health, and Aggressiveness<br>
Aggressiveness works similar to FNAF's movement opportunities,<br>
it take a number 0-100 and if that number is less than the aggressiveness score<br>
then it will hit the cells next to it, if the cell would die then it kills it