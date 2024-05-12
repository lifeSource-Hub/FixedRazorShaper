import random
import Upgrades
import Level

class RazorShaperRedux(Upgrades.RazorShaper):

    def on_init(self):
        Upgrades.RazorShaper.on_init(self)
        self.level = 6
        self.damage = 27

    def get_description(self):
        return ("Whenever you cast a [metallic] spell, deal [{damage}:physical] damage to 1 enemy in line of sight "
                "per spell level.").format(**self.fmt_dict())

    def on_spell_cast(self, evt):
        if Level.Tags.Metallic in evt.spell.tags:
            self.owner.level.queue_spell(self.do_razors(evt))

    def do_razors(self, evt):
        targets = [u for u in self.owner.level.get_units_in_los(evt) if Level.are_hostile(self.owner, u)]
        random.shuffle(targets)

        for t in targets[:evt.spell.level]:
            for p in self.owner.level.get_points_in_line(evt, t)[1:-1]:
                self.owner.level.show_effect(p.x, p.y, Level.Tags.Physical, minor=True)

            t.deal_damage(self.get_stat('damage'), Level.Tags.Physical, self)
            yield

Upgrades.skill_constructors.remove(Upgrades.RazorShaper)
Upgrades.skill_constructors.append(RazorShaperRedux)