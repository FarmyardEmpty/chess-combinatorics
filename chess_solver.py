class ChessBoard:
    def __init__(self):
        self.size = 8
        self.positions = [(i, j) for i in range(self.size) for j in range(self.size)]

    def king_attacks(self, pos):
        attacks = set()
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                x, y = pos[0] + dx, pos[1] + dy
                if 0 <= x < self.size and 0 <= y < self.size:
                    attacks.add((x, y))
        return attacks

    def queen_attacks(self, pos):
        attacks = set()
        for i in range(self.size):
            if i != pos[0]:
                attacks.add((i, pos[1]))
            if i != pos[1]:
                attacks.add((pos[0], i))

        for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            x, y = pos[0] + dx, pos[1] + dy
            while 0 <= x < self.size and 0 <= y < self.size:
                attacks.add((x, y))
                x += dx
                y += dy
        return attacks

    def rook_attacks(self, pos):
        attacks = set()
        for i in range(self.size):
            if i != pos[0]:
                attacks.add((i, pos[1]))
            if i != pos[1]:
                attacks.add((pos[0], i))
        return attacks

    def bishop_attacks(self, pos):
        attacks = set()
        for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            x, y = pos[0] + dx, pos[1] + dy
            while 0 <= x < self.size and 0 <= y < self.size:
                attacks.add((x, y))
                x += dx
                y += dy
        return attacks

    def knight_attacks(self, pos):
        attacks = set()
        moves = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                 (1, 2), (1, -2), (-1, 2), (-1, -2)]

        for dx, dy in moves:
            x, y = pos[0] + dx, pos[1] + dy
            if 0 <= x < self.size and 0 <= y < self.size:
                attacks.add((x, y))
        return attacks

    def is_safe_configuration(self, king_pos, queen_pos, rook_pos, bishop_pos, knight_pos):
        positions = [king_pos, queen_pos, rook_pos, bishop_pos, knight_pos]

        if len(set(positions)) != 5:
            return False

        king_zone = self.king_attacks(king_pos)
        queen_zone = self.queen_attacks(queen_pos)
        rook_zone = self.rook_attacks(rook_pos)
        bishop_zone = self.bishop_attacks(bishop_pos)
        knight_zone = self.knight_attacks(knight_pos)

        if (queen_pos in king_zone or rook_pos in king_zone or
                bishop_pos in king_zone or knight_pos in king_zone):
            return False

        if (king_pos in queen_zone or rook_pos in queen_zone or
                bishop_pos in queen_zone or knight_pos in queen_zone):
            return False

        if (king_pos in rook_zone or queen_pos in rook_zone or
                bishop_pos in rook_zone or knight_pos in rook_zone):
            return False

        if (king_pos in bishop_zone or queen_pos in bishop_zone or
                rook_pos in bishop_zone or knight_pos in bishop_zone):
            return False

        if (king_pos in knight_zone or queen_pos in knight_zone or
                rook_pos in knight_zone or bishop_pos in knight_zone):
            return False

        return True

    def find_all_safe_configurations_optimized(self):
        safe_configs = []
        processed = 0
        total_combinations = 64 ** 5

        print("Поиск безопасных конфигураций...")
        print(f"Всего возможных комбинаций: {total_combinations:,}")

        attack_zones = {}

        for king_pos in self.positions:
            king_zone = self.king_attacks(king_pos)
            attack_zones[('K', king_pos)] = king_zone

            for queen_pos in self.positions:
                if queen_pos == king_pos or queen_pos in king_zone:
                    continue

                queen_zone = self.queen_attacks(queen_pos)
                attack_zones[('Q', queen_pos)] = queen_zone
                if king_pos in queen_zone:
                    continue

                for rook_pos in self.positions:
                    if (rook_pos == king_pos or rook_pos == queen_pos or
                            rook_pos in king_zone or rook_pos in queen_zone):
                        continue

                    rook_zone = self.rook_attacks(rook_pos)
                    attack_zones[('R', rook_pos)] = rook_zone
                    if (king_pos in rook_zone or queen_pos in rook_zone):
                        continue

                    for bishop_pos in self.positions:
                        if (bishop_pos in [king_pos, queen_pos, rook_pos] or
                                bishop_pos in king_zone or bishop_pos in queen_zone or
                                bishop_pos in rook_zone):
                            continue

                        bishop_zone = self.bishop_attacks(bishop_pos)
                        attack_zones[('B', bishop_pos)] = bishop_zone
                        if (king_pos in bishop_zone or queen_pos in bishop_zone or
                                rook_pos in bishop_zone):
                            continue

                        for knight_pos in self.positions:
                            processed += 1

                            if (knight_pos in [king_pos, queen_pos, rook_pos, bishop_pos] or
                                    knight_pos in king_zone or knight_pos in queen_zone or
                                    knight_pos in rook_zone or knight_pos in bishop_zone):
                                continue

                            knight_zone = self.knight_attacks(knight_pos)
                            if (king_pos in knight_zone or queen_pos in knight_zone or
                                    rook_pos in knight_zone or bishop_pos in knight_zone):
                                continue

                            safe_configs.append({
                                'king': king_pos, 'queen': queen_pos,
                                'rook': rook_pos, 'bishop': bishop_pos,
                                'knight': knight_pos
                            })

                            if processed % 1000000 == 0:
                                progress = (processed / total_combinations) * 100
                                print(f"Обработано: {processed:,} ({progress:.2f}%)")

        return safe_configs

if __name__ == "__main__":
        board = ChessBoard()

print("Запуск полного поиска...")
all_safe_configs = board.find_all_safe_configurations_optimized()
print(f"\nВсего безопасных конфигураций: {len(all_safe_configs)}")
