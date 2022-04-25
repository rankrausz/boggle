#####         Boggle game README        #####
#####  by Ran Krausz and Shai Wachtel   #####

This is a simple and fun boggle game, made with Python tkinter module. Enjoy!
To run the game, run boggle.py file

* Words with 2 letters doesn't count. Try harder!

Some added features:

- At any point, if a cube is choosable (by game rules), it will change color to green
  when hovering with the mouse. if not, it won't change color.

- When choosing a cube (by clicking on it), it will change color to orange and add the letter
  to the displayed word below the board. if more than one cube is chosen, only the last cube
  will remain orange while the other change to a brighter color.
  
- You can unchoose only the last cube you chose (the darker orange cube) by clicking on it.
  
- At any point, you can click 'check word' button to see if your word is in the given dictionary.
  if so, the chosen cubes will flash green to let you know that you're right, your score will update
  and you will see the word on the 'Found words' list at the bottom of the window.
  if your word isn't in the dictionary, the chosen cubes will flash red and you can continue playing
  from where you stopped.
  
- To save you time, we've added the 'Clear choice' button to clear all of your currently chosen cubes.

- When you have 20 seconds left, the timer color will change to orange. At 10 seconds left,
  the timer color will change to red.