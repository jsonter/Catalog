from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()



#Menu for UrbanBurger
category1 = Category(name = "Lorem Ipsum")

session.add(category1)
session.commit()

item1 = Item(name = "Lorem Ipsum Dolor Sit Amet", description = "Laboris nisi ut aliquip ex ea commodo consequat. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat. Itaque earum rerum hic tenetur a sapiente delectus. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Totam rem aperiam.", category = category1)

session.add(item1)
session.commit()

item2 = Item(name = "Ipsam Vuptatem", description = "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Corrupti quos dolores et quas molestias excepturi sint occaecati. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat.", category = category1)

session.add(item2)
session.commit()

item3 = Item(name = "Ut Enim", description = "Totam rem aperiam. Excepteur sint occaecat cupidatat non proident, sunt in culpa. Ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat. Nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam. Facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Lorem ipsum dolor sit amet, consectetur adipisicing elit.", category = category1)

session.add(item3)
session.commit()

item4 = Item(name = "Quis Nostrum", description = "Laboris nisi ut aliquip ex ea commodo consequat. Architecto beatae vitae dicta sunt explicabo. Qui officia deserunt mollit anim id est laborum. Inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat.", category = category1)

session.add(item4)
session.commit()

item5 = Item(name = "Itaque Earum Rerum", description = "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam. At vero eos et accusamus. Eaque ipsa quae ab illo inventore veritatis et quasi. Laboris nisi ut aliquip ex ea commodo consequat.", category = category1)

session.add(item5)
session.commit()

item6 = Item(name = "Nam Libero Tempore", description = "Facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Qui officia deserunt mollit anim id est laborum. Eaque ipsa quae ab illo inventore veritatis et quasi. Laboris nisi ut aliquip ex ea commodo consequat. Ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat.", category = category1)

session.add(item6)
session.commit()

item7 = Item(name = "At Vero", description = "Facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Qui officia deserunt mollit anim id est laborum.", category = category1)

session.add(item7)
session.commit()

item8 = Item(name = "Temporibus Autem Quibusdam", description = "Inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam. Inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam.", category = category1)

session.add(item8)
session.commit()




#Menu for Super Stir Fry
category2 = Category(name = "Star Wars")

session.add(category2)
session.commit()


item1 = Item(name = "Knights of the Old Republic", description = "Kid, I've flown from one side of this galaxy to the other. I've seen a lot of strange stuff, but I've never seen anything to make me believe there's one all-powerful Force controlling everything. There's no mystical energy field that controls my destiny. It's all a lot of simple tricks and nonsense. I can't get involved! I've got work to do! It's not that I like the Empire, I hate it, but there's nothing I can do about it right now. It's such a long way from here. Remember, a Jedi can feel the Force flowing through him. You don't believe in the Force, do you? I need your help, Luke. She needs your help. I'm getting too old for this sort of thing.", category = category2)

session.add(item1)
session.commit()

item2 = Item(name = "Peking Duck", description = " A famous duck dish from Beijing[1] that has been prepared since the imperial era. The meat is prized for its thin, crisp skin, with authentic versions of the dish serving mostly the skin and little meat, sliced in front of the diners by the cook", category = category2)

session.add(item2)
session.commit()

item3 = Item(name = "Jedi Academy", description = "What!? You don't believe in the Force, do you? You don't believe in the Force, do you? Kid, I've flown from one side of this galaxy to the other. I've seen a lot of strange stuff, but I've never seen anything to make me believe there's one all-powerful Force controlling everything. There's no mystical energy field that controls my destiny. It's all a lot of simple tricks and nonsense. You don't believe in the Force, do you?", category = category2)

session.add(item3)
session.commit()

item4 = Item(name = "The Rebel Force", description = "No! Alderaan is peaceful. We have no weapons. You can't possibly... What!? I need your help, Luke. She needs your help. I'm getting too old for this sort of thing. You mean it controls your actions? Kid, I've flown from one side of this galaxy to the other. I've seen a lot of strange stuff, but I've never seen anything to make me believe there's one all-powerful Force controlling everything. There's no mystical energy field that controls my destiny. It's all a lot of simple tricks and nonsense.", category = category2)

session.add(item4)
session.commit()

item5 = Item(name = "The Phantom Menace", description = "Escape is not his plan. I must face him, alone. You mean it controls your actions? In my experience, there is no such thing as luck. What good is a reward if you ain't around to use it? Besides, attacking that battle station ain't my idea of courage. It's more like...suicide.", category = category2)

session.add(item5)
session.commit()

item6 = Item(name = "A New Hope", description = "Partially, but it also obeys your commands. What good is a reward if you ain't around to use it? Besides, attacking that battle station ain't my idea of courage. It's more like...suicide. You don't believe in the Force, do you? Partially, but it also obeys your commands. Kid, I've flown from one side of this galaxy to the other. I've seen a lot of strange stuff, but I've never seen anything to make me believe there's one all-powerful Force controlling everything. There's no mystical energy field that controls my destiny. It's all a lot of simple tricks and nonsense.", category = category2)

session.add(item6)
session.commit()


#Menu for Panda Garden
category1 = Category(name = "The Simpsons")

session.add(category1)
session.commit()


item1 = Item(name = "Homer the Great", description = "Uh, no, you got the wrong number. This is 9-1...2. D'oh. Thank you, steal again. Kids, kids. I'm not going to die. That only happens to bad people. But, Aquaman, you cannot marry a woman without gills. You're from two different worlds... Oh, I've wasted my life.", category = category1)

session.add(item1)
session.commit()

item2 = Item(name = "Marge vs. Monorail", description = "I didn't get rich by signing checks. Our differences are only skin deep, but our sames go down to the bone. D'oh.", category = category1)

session.add(item2)
session.commit()

item3 = Item(name = "The Last Temptation of Homer", description = "Get ready, skanks! It's time for the truth train! Our differences are only skin deep, but our sames go down to the bone. I've done everything the Bible says - even the stuff that contradicts the other stuff! Our differences are only skin deep, but our sames go down to the bone.", category = category1)

session.add(item3)
session.commit()

item4 = Item(name = "Homer: Bad Man", description = "Our differences are only skin deep, but our sames go down to the bone. Fire can be our friend; whether it's toasting marshmallows or raining down on Charlie. Don't kid yourself, Jimmy. If a cow ever got the chance, he'd eat you and everyone you care about! Oh, loneliness and cheeseburgers are a dangerous mix. Get ready, skanks! It's time for the truth train! Save me, Jeebus.", category = category1)

session.add(item4)
session.commit()

item2 = Item(name = "Life on the Fast Lane", description = "Please do not offer my god a peanut. Save me, Jeebus. Get ready, skanks! It's time for the truth train! Uh, no, you got the wrong number. This is 9-1...2.", category = category1)

session.add(item2)
session.commit()


#Menu for Thyme for that
category1 = Category(name = "Monty Python")

session.add(category1)
session.commit()


item1 = Item(name = "Makes Ben Hur look like an Epic", description = "Shut up! Will you shut up?! Well, what do you want? I dunno. Must be a king. No, no, no! Yes, yes. A bit. But she's got a wart. He hasn't got shit all over him. ...Are you suggesting that coconuts migrate?", category = category1)

session.add(item1)
session.commit()

item2 = Item(name = "How do you know she is a witch?", description = "I have to push the pram a lot. But you are dressed as one... Oh! Come and see the violence inherent in the system! Help, help, I'm being repressed! Who's that then? I don't want to talk to you no more, you empty-headed animal food trough water! I fart in your general direction! Your mother was a hamster and your father smelt of elderberries! Now leave before I am forced to taunt you a second time! Knights of Ni, we are but simple travelers who seek the enchanter who lives beyond these woods.", category = category1)

session.add(item2)
session.commit()

item3 = Item(name = "King Arthur", description = "Knights of Ni, we are but simple travelers who seek the enchanter who lives beyond these woods. She looks like one. But you are dressed as one... Shut up! Will you shut up?! Who's that then?", category = category1)

session.add(item3)
session.commit()

item4 = Item(name = "What... is your quest?", description = "I dunno. Must be a king. The Lady of the Lake, her arm clad in the purest shimmering samite, held aloft Excalibur from the bosom of the water, signifying by divine providence that I, Arthur, was to carry Excalibur. That is why I am your king. Well, what do you want? Shut up! But you are dressed as one... Look, my liege!", category = category1)

session.add(item4)
session.commit()

item5 = Item(name = "Blue. No, yel...", description = "It's only a model. Now, look here, my good man. Shh! Knights, I bid you welcome to your new home. Let us ride to Camelot! Oh! Come and see the violence inherent in the system! Help, help, I'm being repressed!", category = category1)

session.add(item5)
session.commit()

item2 = Item(name = "First shalt thou take out the Holy Pin", description = "I don't want to talk to you no more, you empty-headed animal food trough water! I fart in your general direction! Your mother was a hamster and your father smelt of elderberries! Now leave before I am forced to taunt you a second time! Shh! Knights, I bid you welcome to your new home. Let us ride to Camelot! Well, we did do the nose. Knights of Ni, we are but simple travelers who seek the enchanter who lives beyond these woods. Well, how'd you become king, then? Well, Mercia's a temperate zone!", category = category1)

session.add(item2)
session.commit()



#Menu for Tony's Bistro
category1 = Category(name = "Futurama")

session.add(category1)
session.commit()


item1 = Item(name = "Godfellas", description = "Um, is this the boring, peaceful kind of taking to the streets? Shut up and get to the point! Tell her you just want to talk. It has nothing to do with mating. Tell her you just want to talk. It has nothing to do with mating.", category = category1)

session.add(item1)
session.commit()

item2 = Item(name = "A Clone of My Own", description = "All I want is to be a monkey of moderate intelligence who wears a suit... that's why I'm transferring to business school! We don't have a brig. These old Doomsday Devices are dangerously unstable. I'll rest easier not knowing where they are. You won't have time for sleeping, soldier, not with all the bed making you'll be doing.",  category = category1)

session.add(item2)
session.commit()

item3 = Item(name = "Anthology of Interest II", description = "But I've never been to the moon! Oh Leela! You're the only person I could turn to; you're the only person who ever loved me. Well, thanks to the Internet, I'm now bored with sex. Is there a place on the web that panders to my lust for violence?", category = category1)

session.add(item3)
session.commit()

item4 = Item(name = "A Big Piece of Garbage", description = "Who said that? SURE you can die! You want to die?! Soothe us with sweet lies. I had more, but you go ahead.", category = category1)

session.add(item4)
session.commit()

item5 = Item(name = "Time Keeps on Slippin'", description = "And when we woke up, we had these bodies. That's not soon enough! Bite my shiny metal ass. Negative, bossy meat creature! Is the Space Pope reptilian!?", category = category1)

session.add(item5)
session.commit()



print "added menu items!"
