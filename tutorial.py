

# tutorial file 
# As an admin, the app has access to read and write all data, regradless of Security Rules
# ref = db.reference('server/saving-data/fireblog')
# users_ref = ref.child('users')
# users_ref.set({
#     'alanisawesome': {
#         'date_of_birth': 'June 23, 1912',
#         'full_name': 'Alan Turing'
#     },
#     'gracehop': {
#         'date_of_birth': 'December 9, 1906',
#         'full_name': 'Grace Hopper'
#     }
# })

# users_ref.child('alanisawesome').set({
#     'date_of_birth': 'June 23, 1912',
#     'full_name': 'Alan Turing'
# })
# users_ref.child('gracehop').set({
#     'date_of_birth': 'December 9, 1906',
#     'full_name': 'Grace Hopper'
# })

# posts_ref = ref.child('posts')

# new_post_ref = posts_ref.push()
# new_post_ref.set({
#     'author': 'gracehop',
#     'title': 'Announcing COBOL, a New Programming Language'
# })

# # We can also chain the two calls together
# posts_ref.push().set({
#     'author': 'alanisawesome',
#     'title': 'The Turing Machine'
# })

