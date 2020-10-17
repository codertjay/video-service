Model Architecture planning

Membership Model
    -slug / course-number-1
    -type (choices, free pro enterprise)
    -price
    -stripe plan id 
    
    
UserMembership Model
    -user                        (foreignkey to the default user)
    -stripe customer id 
    -membership type                 (foreignkey to the default Membership )
    
subscription
    -user memebership
    -stripe subscription id   (foreignkey to the default user)(this is only when a user have create a subscription)
    -active
    
Course
    -slug
    -title
    -description
    -allowed memberships  (foreignkey to Membership)
    
Lesson
    -slug   
    -title
    -course   (foreignkey to course)
    -position 
    -video
    -thumbnail

    
