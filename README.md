# JL
takehome


## Error that I found

In the PDF file given, I found that twitter username is given the range of 55 to 66 that renders `@elversatil` (without the ending 'e'), which makes no sense. Therefore, I've altered it to the range of 55 to 67 which renders `@elversatile` and have an '@' checking method built in to the Username class to verify the validity of a username

## Design document/explanation
**a. Input Object**

For the sake of this takehomes's main purpsoe: decorate **ALL** of the word element, I design the input to be an object of the following `ProcessedTweet()` class to have the highest efficiency. In `ProcessedTweet()` class:

1. `fullText`: A string containing the original full text
2. `elements`: A list of tuples, eg. (starting index, ending index, element type). This list is designed to be a **min-heap**

3. `setFullText()`: A method to set the original text
4. `appendElement()`: A method to append newly defined element into the list. Take **O(lgN)** time for each increment. 
5. `popFrontElement()`: A method to get the element in the front of the original string (fullText).  The structure I used in the class is a min-heap so this method will pop the element one after another in accending order, ordered by starting index. Takes **O(lgN)** time for each operation


**b. Element Class**

`Element` is a parent class for any current and future elements. Eg. Entity, Username, Link, and potentially hashtag. I designed the class to have the following methods:

1. `setFullText()`: setter of the (private) variable `fullText`, Str
2. `setText()`: setter of the (private) variable `text`, Str
3. `setStart()`: setter of the (private) variable `start`, INT
4. `setEnd()`: setter of the (private) variable `end`, INT
5. `setDecorator()`: static method that set the static variable `decorator`, and Decorator object
6. `decorate()`: call the decorator object and return a decorated string
7. `checkRange()`: check the validity of the range of start and end


**c. Entity Class**

1. Inherit from `Element` Class
2. Override the parent class with 3 initial arguments
3. Set initial variables and implement `checkRange()` while constructing
4. Set the static decorator to a `HtmlEntityDecorator` instance
5. Override static function `setDecorator()`


**d. Username Class**

1. Inherit from `Element` Class. 
2. Override the parent class with 3 initial arguments. 
3. Extend the parent class with a method `checkAt()` to constrain/verify the format of a username. 
4. Set initial variables and implement `checkRange()` and `checkAt()` while constructing.
5. Set the static decorator to a `HtmlUsernameDecorator` instance
6. Override static function `setDecorator()`


**e. Link Class**
	
1. Inherit from `Element` Class
2. Override the parent class with 3 initial arguments
3. Set initial variables and implement `checkRange()` while constructing
4. Set the static decorator to a `HtmlLinkDecorator` instance
5. Override static function `setDecorator()`


**f. Decorator Interface**

`Decorator` is an interface implemented by different kinds of syntex decorator. Eg. Html, or perhaps markdown...etc. For this takehome, I created only a `HtmlDecorator` class to implement the interface. However, this interface is designed to be be implemented by many other kinds of decorators in the future. For example, one could design a class `MarkdownDecorator()` to make the element bold in markdown syntax by decorating the element as "**text**" or "__text__". There are only 2 required method in this interface.

1. `setText()`: set the text to be decorated
2. `decorate()`: return the decorated the text

**g. HtmlDecorator Class**

Implement `Decorator` interface. This is extended with 1 setter method, `setTag()` and implement 2 methods in the interface.

1. `setText()`: set the text to be decorated to the (private) variable, text
2. `setTag()`: set the html tag to decorate the text to the (private) variable, tag
3. `decorate()`: decorate the text in a basic html style: only adding the tag to the front and back of the text without any html attributes. Return a string


**h. HtmlEntityDecorator Class**

Inherit from `HtmlDecorator` Class. Set the (private) variable tag to 'strong' while constructing.

**i. HtmlUsernameDecorator Class**

Inherit from `HtmlDecorator` Class. Set the (private) variable tag to 'a' while constructing. Override the method `decorate()` with adding a html attribute 'href' to the front tag, seperating the '@' from the username and put it in front of the front tag.

**j. HtmlLinkDecorator Class**

Inherit from `HtmlDecorator` Class. Set the (private) variable tag to 'a' while constructing. Override the method `decorate()` with adding a html attribute 'href' to the front tag


## Future Extention 

**a. Adding new Elements**

All other elements could and should implement from `Element` class. One can override the `Element` class to have some default setting on newly designed element class. For example, one could design a `Markdown` class and set the default decorator to `MarkdownDecorator` object.


**b. Changing Decorating Rule Dynamically**

Since there should only be 1 set of decorating rule for each type of element throughout a single input object(tweet) conversion. I designed the decorator attribute to be static. To change the default decorating rule for an element type, one could simply use the static method `setDecorator()` given to every element class to set the decorator for the class. The change will appears on all existing and future instance(Assumed before the other alternation). For example,

```
exampleEntity = Entity('sometext', 0, 4)
print exampleEntity.decorate() #Using the default decorator
```
will output `<strong>some</strong>`
Adding the following lines:

```
d = HtmlDecorator()
d.setTag('div')
Entity.setDecorator(d)
print exampleEntity.decorate()  #Using the the d decorator(HtmlDecorator)
```

will output `<div>some</div>`
And continue adding the following lines:

```
exampleEntity2 = Entity('helloworld', 0, 5)
print exampleEntity2.decorate() #Using the the d decorator(HtmlDecorator)
```

will output `<div>hello</div>`

Also, to expend even wider, one could even assign different syntax decorator to an element type. For example,


```
d = MarkdownDecorator('bold')  #This MarkdownDecorator() class should be designed elsewhere
Entity.setDecorator(d)
print exampleEntity.decorate()
```

this could output `**some**`
	

To add a new syntax decorating rule, one should implement a decorator from `Decorator` interface


**d. Add new Element-specific Actions**

This is outside of the scope of this takehome; yet, this is the reason that I create a class for each type of element. In case that some day in the future, some other actions other than decoration is need, it's easier to extend my code and define actions for each type of data. For example, one could store the 'username' into the database by adding a method of `storeToDatabase()` to the `Username` class, and utilize it by using is as `username.storeToDatabase()` 

Another example is to shorten the link. One could add a method `shortUrl()` into the `Link` class, and utilize it by `link.shortUrl()`.

Plain and simple.

**e. Imaginary Scenario: Add a new type 'hashtag' (In General Steps)**

1. Create a new decorator class, `HtmlHashtagDecorator`, inherited from `HtmlDecorator`. Override the `decorate()` method
2. Create a new element class, `Hashtag`, configure and instantize `HtmlHashtagDecorator`, and set the default decorator of the class `Hashtag` to the instantized `HtmlHashtagDecorator` object. Override the static `setDecorator()` method
3. Configure and instantize `Hashtag`, get the output by `hashtag.decorate()`


## Error Proof Mechanisms

1. Error raising mechanism
2. Setter and getter methods, eg. appendElement(), and popFrontElement() (provide protection to private variables)
3. Interface design (prevent missing required methods)
4. Behavior object design (provide prection to dynamic behavior changing)
5. Static variable and method design (enforce consistency)




