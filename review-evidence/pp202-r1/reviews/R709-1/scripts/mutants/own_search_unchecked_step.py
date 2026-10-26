# the search takes the candidate after a hit without testing it (a colliding new ID)
OLD = "          if (!sid_hit_w) begin\n            state_r <= S_EV_ACT;\n          end\n        end\n\n        S_EV_ACT: begin"
NEW = "          state_r <= S_EV_ACT;\n        end\n\n        S_EV_ACT: begin"
