from edge_functions.dice_logic import dice_sides as ds

boost_die = [ds.blank, ds.blank, ds.success, ds.success+ds.advantage, ds.advantage+ds.advantage, ds.advantage]

set_back_die = [ds.blank, ds.fail, ds.threat]

ability_die = [ds.blank, ds.success, ds.success, ds.success+ds.success, ds.advantage, ds.advantage,
               ds.success+ds.advantage, ds.advantage+ds.advantage]

difficulty_die = [ds.blank, ds.fail, ds.fail+ds.fail, ds.threat, ds.threat, ds.threat, ds.threat+ds.threat,
                  ds.fail+ds.threat]

proficiency_die = [ds.blank, ds.success, ds.success, ds.success+ds.success, ds.success+ds.success, ds.advantage,
                   ds.success+ds.advantage, ds.success+ds.advantage, ds.success+ds.advantage, ds.advantage+ds.advantage,
                   ds.advantage+ds.advantage, ds.triumph]

challenge_die = [ds.blank, ds.fail, ds.fail, ds.fail+ds.fail, ds.fail+ds.fail, ds.threat, ds.threat, ds.fail+ds.threat,
                 ds.fail+ds.threat, ds.threat+ds.threat, ds.threat+ds.threat, ds.despair]

force_die = [ds.dark, ds.dark, ds.dark, ds.dark, ds.dark, ds.dark, ds.dark+ds.dark, ds.light, ds.light,
             ds.light+ds.light, ds.light+ds.light, ds.light+ds.light]
